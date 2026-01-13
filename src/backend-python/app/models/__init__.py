from .gpr import GPRRecord, WeeklyReport, Material, Customer, ProjectObject
from .documents import Document, DocumentType, DocumentShipment, DocumentReturn
from .files import FileCategory, UploadedFile, MaterialRequest, MaterialStock
from .user import User, UserSession
from .work_session import WorkSession
from .construction_remarks import ConstructionRemark, RemarkPhoto, RemarkHistory, add_remarks_relationship

# Добавляем связь к модели ProjectObject
add_remarks_relationship()