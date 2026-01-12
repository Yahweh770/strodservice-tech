from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime
import logging

from ..services.material_notification_service import MaterialNotificationService
from .. import crud, models

logger = logging.getLogger(__name__)

# Сопоставление типов работ (work_type) с необходимыми материалами
MATERIAL_REQUIREMENTS = {
    "kraska_b": {"material_id": 1, "quantity_per_unit": 1},  # Краска б
    "kraska_ch": {"material_id": 2, "quantity_per_unit": 1}, # Краска ч
    "vremyanka": {"material_id": 3, "quantity_per_unit": 1}, # Времянка
    "kraska_j": {"material_id": 4, "quantity_per_unit": 1},  # Краска ж
    "hp": {"material_id": 5, "quantity_per_unit": 1},        # ХП
    "hpj": {"material_id": 6, "quantity_per_unit": 1},       # ХПж
    "tp": {"material_id": 7, "quantity_per_unit": 1},        # ТП
    "demarkirovka": {"material_id": 8, "quantity_per_unit": 1} # Демаркировка
}


def check_materials_for_work(db: Session, gpr_record_id: int) -> Dict[str, Any]:
    """
    Проверяет наличие материалов для выполнения работ по ГПР записи
    """
    gpr_record = crud.get_gpr_record(db, gpr_record_id)
    if not gpr_record:
        return {"status": "error", "message": "Запись ГПР не найдена"}
    
    # Получаем требуемые материалы для типа работ
    work_type = gpr_record.work_type
    if work_type not in MATERIAL_REQUIREMENTS:
        return {"status": "warning", "message": f"Тип работ {work_type} не имеет определенных требований к материалам"}
    
    material_req = MATERIAL_REQUIREMENTS[work_type]
    material_id = material_req["material_id"]
    required_quantity = gpr_record.volume_plan * material_req["quantity_per_unit"]
    
    # Проверяем наличие материала
    stock = crud.get_material_stock_by_material(db, material_id)
    
    if stock:
        available = stock.quantity - stock.reserved_quantity
        shortage = max(0, required_quantity - available)
        
        result = {
            "status": "checked",
            "work_type": work_type,
            "material_id": material_id,
            "required_quantity": required_quantity,
            "available_quantity": available,
            "shortage": shortage,
            "needs_order": shortage > 0
        }
        
        # Если не хватает материалов, создаем запрос на закупку
        if shortage > 0:
            service = MaterialNotificationService(db)
            required_materials = {material_id: required_quantity}
            notifications = service.check_material_needs_for_section(
                section_id=f"gpr_{gpr_record_id}",
                required_materials=required_materials
            )
            
            result["notifications"] = notifications
            result["message"] = f"Необходимо заказать {shortage} единиц материала для выполнения работ"
        else:
            result["message"] = "Материалов достаточно для выполнения работ"
        
        return result
    else:
        # Создаем запись о складе с нулевым остатком
        from ..schemas import MaterialStockCreate
        stock_data = MaterialStockCreate(
            material_id=material_id,
            quantity=0,
            min_threshold=10
        )
        crud.create_material_stock(db, stock_data)
        
        # Создаем запрос на закупку
        service = MaterialNotificationService(db)
        required_materials = {material_id: required_quantity}
        notifications = service.check_material_needs_for_section(
            section_id=f"gpr_{gpr_record_id}",
            required_materials=required_materials
        )
        
        return {
            "status": "checked",
            "work_type": work_type,
            "material_id": material_id,
            "required_quantity": required_quantity,
            "available_quantity": 0,
            "shortage": required_quantity,
            "needs_order": True,
            "notifications": notifications,
            "message": f"Нет материала на складе, необходимо заказать {required_quantity} единиц"
        }


def reserve_materials_for_gpr_work(db: Session, gpr_record_id: int) -> bool:
    """
    Резервирует материалы для выполнения работ по ГПР
    """
    result = check_materials_for_work(db, gpr_record_id)
    
    if result["status"] == "checked" and result["needs_order"] == False:
        # Резервируем материалы
        service = MaterialNotificationService(db)
        material_requirements = {result["material_id"]: result["required_quantity"]}
        
        return service.reserve_materials_for_section(
            section_id=f"gpr_{gpr_record_id}",
            material_requirements=material_requirements
        )
    
    return False


def update_material_usage(db: Session, gpr_record_id: int, work_volume: float):
    """
    Обновляет использование материалов после выполнения работ
    """
    gpr_record = crud.get_gpr_record(db, gpr_record_id)
    if not gpr_record:
        return False
    
    work_type = gpr_record.work_type
    if work_type not in MATERIAL_REQUIREMENTS:
        return True  # Пропускаем, если тип работы не требует материалов
    
    material_req = MATERIAL_REQUIREMENTS[work_type]
    material_id = material_req["material_id"]
    consumed_quantity = work_volume * material_req["quantity_per_unit"]
    
    # Обновляем остаток на складе
    stock = crud.get_material_stock_by_material(db, material_id)
    if stock and stock.quantity >= consumed_quantity:
        stock.quantity -= consumed_quantity
        # Также уменьшаем зарезервированное количество, если оно было
        if stock.reserved_quantity >= consumed_quantity:
            stock.reserved_quantity -= consumed_quantity
        db.commit()
        return True
    
    return False


def initialize_material_stocks(db: Session):
    """
    Инициализирует складские остатки для всех материалов
    """
    # Получаем справочник материалов
    from ..models.gpr import MATERIALS_REFERENCE
    
    for idx, mat_data in enumerate(MATERIALS_REFERENCE, start=1):
        # Проверяем, существует ли уже запись
        existing_stock = crud.get_material_stock_by_material(db, idx)
        if not existing_stock:
            # Создаем новую запись со стандартными значениями
            from ..schemas import MaterialStockCreate
            stock_data = MaterialStockCreate(
                material_id=idx,
                quantity=0,  # Начальный остаток
                min_threshold=10,  # Минимальный порог
                location="Основной склад"
            )
            crud.create_material_stock(db, stock_data)
            logger.info(f"Создана начальная запись о складе для материала {mat_data['name']}")
    
    db.commit()
    logger.info("Инициализация складских остатков завершена")