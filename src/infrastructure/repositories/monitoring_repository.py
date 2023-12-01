import uuid
from sqlalchemy.orm import Session
from typing import Callable, Optional
from domain.repositories.monitoring_repository import MonitoringRepository as repository
from infrastructure.repositories.db_model.monitoring_db import MonitoringDb

class MonitoringRepository:

    database: Callable[[], Session]

    def __init__(self, session = Callable[[], Session]):
        self.database = session
    
    def save(self, id_satellite: str) -> None:
        session = self.database()
        monitoring = MonitoringDb()
        monitoring.id= uuid.uuid4().hex
        monitoring.id_satellite = id_satellite
        session.merge(monitoring)
        session.commit()
    
    def find_first(self) -> Optional[str]:
        session = self.database()
        data = session.query(MonitoringDb).first()
        
        return data.id_satellite
    

assert isinstance(MonitoringRepository({}), repository)