from sqlalchemy.orm import Session
from datetime import datetime
import logging
from typing import List

from .. import crud, models, schemas
from ..database import get_db

logger = logging.getLogger(__name__)


class MaterialNotificationService:
    """
    Сервис для автоматического уведомления менеджера о необходимости заказа материалов
    """
    
    def __init__(self, db: Session):
        self.db = db
        
    def check_low_stock_and_notify(self) -> List[dict]:
        """
        Проверяет уровень остатков материалов и уведомляет менеджера о необходимости заказа
        """
        low_stock_materials = crud.get_low_stock_materials(self.db)
        
        notifications = []
        for item in low_stock_materials:
            material = item['material']
            current_stock = item['current_stock']
            min_threshold = item['min_threshold']
            
            # Создаем запрос на закупку материала
            request_data = schemas.MaterialRequestCreate(
                material_id=material.id,
                requested_quantity=min_threshold,  # Запрашиваем до минимального порога
                needed_quantity=min_threshold,
                available_quantity=current_stock,
                reason=f"Автоматическое уведомление: уровень запаса {current_stock} ниже минимального порога {min_threshold}",
                requested_by="system"
            )
            
            # Проверяем, существует ли уже активный запрос на этот материал
            existing_requests = self.db.query(models.MaterialRequest).filter(
                models.MaterialRequest.material_id == material.id,
                models.MaterialRequest.status.in_(["pending", "approved"])
            ).all()
            
            if not existing_requests:
                # Создаем новый запрос на закупку
                new_request = crud.create_material_request(self.db, request_data)
                
                notification = {
                    "material_name": material.name,
                    "material_id": material.id,
                    "current_stock": current_stock,
                    "min_threshold": min_threshold,
                    "requested_quantity": min_threshold,
                    "request_id": new_request.id,
                    "message": f"Материал '{material.name}' требует пополнения: текущий запас {current_stock}, минимальный порог {min_threshold}"
                }
                
                notifications.append(notification)
                logger.info(f"Создан запрос на закупку материала: {notification['message']}")
            else:
                logger.info(f"Активный запрос на материал '{material.name}' уже существует")
        
        return notifications
    
    def check_material_needs_for_section(self, section_id: str, required_materials: dict) -> List[dict]:
        """
        Проверяет наличие материалов для определенной секции и создает запросы при необходимости
        """
        notifications = []
        
        for material_id, needed_quantity in required_materials.items():
            stock = crud.get_material_stock_by_material(self.db, material_id)
            
            if stock:
                available = stock.quantity - stock.reserved_quantity
                if available < needed_quantity:
                    # Нужно заказать дополнительные материалы
                    shortage = needed_quantity - available
                    
                    # Проверяем, есть ли уже активный запрос
                    existing_requests = self.db.query(models.MaterialRequest).filter(
                        models.MaterialRequest.material_id == material_id,
                        models.MaterialRequest.status.in_(["pending", "approved"]),
                        models.MaterialRequest.section_id == section_id
                    ).all()
                    
                    if not existing_requests:
                        request_data = schemas.MaterialRequestCreate(
                            material_id=material_id,
                            requested_quantity=shortage,
                            needed_quantity=needed_quantity,
                            available_quantity=available,
                            section_id=section_id,
                            reason=f"Необходимость в работе секции {section_id}: требуется {needed_quantity}, доступно {available}",
                            requested_by="system"
                        )
                        
                        new_request = crud.create_material_request(self.db, request_data)
                        
                        notification = {
                            "section_id": section_id,
                            "material_id": material_id,
                            "needed_quantity": needed_quantity,
                            "available_quantity": available,
                            "shortage": shortage,
                            "request_id": new_request.id,
                            "message": f"Секция {section_id} нуждается в материале {material_id}: требуется {needed_quantity}, доступно {available}"
                        }
                        
                        notifications.append(notification)
                        logger.info(f"Создан запрос на закупку для секции: {notification['message']}")
            else:
                # Если складской записи нет, создаем ее с нулевым остатком
                stock_data = schemas.MaterialStockCreate(
                    material_id=material_id,
                    quantity=0,
                    min_threshold=10
                )
                crud.create_material_stock(self.db, stock_data)
                
                # Создаем запрос на закупку
                request_data = schemas.MaterialRequestCreate(
                    material_id=material_id,
                    requested_quantity=needed_quantity,
                    needed_quantity=needed_quantity,
                    available_quantity=0,
                    section_id=section_id,
                    reason=f"Необходимость в работе секции {section_id}: требуется {needed_quantity}, доступно 0",
                    requested_by="system"
                )
                
                new_request = crud.create_material_request(self.db, request_data)
                
                notification = {
                    "section_id": section_id,
                    "material_id": material_id,
                    "needed_quantity": needed_quantity,
                    "available_quantity": 0,
                    "request_id": new_request.id,
                    "message": f"Секция {section_id} нуждается в материале {material_id}: требуется {needed_quantity}, доступно 0"
                }
                
                notifications.append(notification)
                logger.info(f"Создан первый запрос на закупку материала: {notification['message']}")
        
        return notifications
    
    def reserve_materials_for_section(self, section_id: str, material_requirements: dict) -> bool:
        """
        Резервирует материалы для определенной секции
        """
        try:
            for material_id, quantity in material_requirements.items():
                stock = crud.get_material_stock_by_material(self.db, material_id)
                
                if stock:
                    available = stock.quantity - stock.reserved_quantity
                    if available >= quantity:
                        # Резервируем материалы
                        stock.reserved_quantity += quantity
                        self.db.commit()
                        logger.info(f"Зарезервировано {quantity} единиц материала {material_id} для секции {section_id}")
                    else:
                        logger.warning(f"Недостаточно материалов {material_id} для резервирования в секции {section_id}")
                        return False
                else:
                    logger.warning(f"Нет информации о складском запасе материала {material_id}")
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Ошибка при резервировании материалов: {str(e)}")
            self.db.rollback()
            return False
    
    def release_reserved_materials(self, section_id: str, material_requirements: dict):
        """
        Освобождает зарезервированные материалы
        """
        try:
            for material_id, quantity in material_requirements.items():
                stock = crud.get_material_stock_by_material(self.db, material_id)
                
                if stock and stock.reserved_quantity >= quantity:
                    stock.reserved_quantity -= quantity
                    self.db.commit()
                    logger.info(f"Освобождено {quantity} единиц материала {material_id} из резерва")
        except Exception as e:
            logger.error(f"Ошибка при освобождении зарезервированных материалов: {str(e)}")
            self.db.rollback()


# Функция для периодической проверки остатков (может быть вызвана из внешнего планировщика)
def run_material_check():
    """
    Функция для периодического запуска проверки остатков материалов
    """
    from ..database import SessionLocal
    
    db = SessionLocal()
    try:
        service = MaterialNotificationService(db)
        notifications = service.check_low_stock_and_notify()
        
        if notifications:
            print(f"Найдено {len(notifications)} материалов, требующих пополнения:")
            for notification in notifications:
                print(f"- {notification['message']}")
        else:
            print("Все материалы находятся в пределах нормы")
            
    finally:
        db.close()


if __name__ == "__main__":
    run_material_check()