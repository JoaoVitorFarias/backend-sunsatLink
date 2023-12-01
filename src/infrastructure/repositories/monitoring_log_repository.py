import uuid
from sqlalchemy.orm import Session
from typing import Callable
from application.model.satellite_log import SatelliteLog
from domain.repositories.monitoring_log_repository import MonitoringLogRepository as repository
from infrastructure.repositories.db_model.monitoring_log_db import MonitoringLogDb

class MonitoringLogRepository:

    database: Callable[[], Session]

    def __init__(self, session = Callable[[], Session]):
        self.database = session
    
    def save(self, log: SatelliteLog) -> None:
        data = MonitoringLogDb()
        data.id = uuid.uuid4().hex
        data.name = log.name
        data.id_provider = log.id_provider
        data.is_favorite = log.is_favorite
        data.time = log.time

        session = self.database()
        session.merge(data)
        session.commit()
    
    def find_all(self) -> list[SatelliteLog]:
        session = self.database()
        data = session.query(MonitoringLogDb).all()
        
        list_data = []
        for sat in data:
            log = SatelliteLog()
            log.id = sat.id
            log.id_provider = sat.id_provider
            log.name = sat.name
            log.is_favorite = sat.is_favorite
            log.time = sat.time

            list_data.append(log)

        return list_data
    

assert isinstance(MonitoringLogRepository({}), repository)