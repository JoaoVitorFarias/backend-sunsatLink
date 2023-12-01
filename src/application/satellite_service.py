
from application.model.satellite_log import SatelliteLog
from domain.entities.satellite import Satellite
from domain.repositories.monitoring_log_repository import MonitoringLogRepository
from domain.repositories.monitoring_repository import MonitoringRepository
from domain.repositories.satellite_repository import SatelliteRepository
import uuid


class SatelliteService():
    __satellite_repository__: SatelliteRepository
    __monitoring_repository__: MonitoringRepository
    __log_repository__: MonitoringLogRepository

    def __init__(
        self,
        satellite_repository: SatelliteRepository,
        monitoring_repository: MonitoringRepository,
        log_repository: MonitoringLogRepository
    ):
        self.__satellite_repository__ = satellite_repository
        self.__monitoring_repository__ = monitoring_repository
        self.__log_repository__ = log_repository
        
    def save(self, satellite: Satellite) -> Satellite:
        satellite.id = uuid.uuid4().hex

        return self.__satellite_repository__.save(satellite)

    def delete(self, satellite:Satellite) -> None:
        self.__satellite_repository__.delete(satellite)

    def save_monitoring(self, id_satellite: str) -> None:
        self.__monitoring_repository__.save(id_satellite)

    def save_monitoring_log(self, satellite: SatelliteLog):
        self.__log_repository__.save(satellite)