from datetime import datetime
from application.api_satellite_service import ApiSatelliteService
from application.model.satellite_log import SatelliteLog
from application.model.satellite_trajectory import SatelliteTrajectory
from application.model.satellite_with_position_model import SatelliteWithPositionModel
from application.model.satellite_with_positions_model import SatelliteWithPositionsModel
from application.satellite_service import SatelliteService
from domain.entities.satellite import Satellite
from domain.repositories.monitoring_log_repository import MonitoringLogRepository
from domain.repositories.monitoring_repository import MonitoringRepository
from domain.repositories.satellite_repository import SatelliteRepository


class SatelliteQueryService():
    __satellite_repository__: SatelliteRepository
    __api_satellite_service__: ApiSatelliteService
    __monitoring_repository__: MonitoringRepository
    __satellite_service__: SatelliteService 
    __log_repository__: MonitoringLogRepository

    def __init__(
        self,
        satellite_repository: SatelliteRepository,
        api_satellite_service: ApiSatelliteService,
        monitoring_repository: MonitoringRepository,
        satellite_service: SatelliteService,
        log_repository: MonitoringLogRepository
    ):
        self.__satellite_repository__ = satellite_repository
        self.__api_satellite_service__ = api_satellite_service
        self.__monitoring_repository__ = monitoring_repository
        self.__satellite_service__ = satellite_service
        self.__log_repository__ = log_repository

    def find_all_by_category(self, category_id: str, filter=None) -> list[SatelliteWithPositionModel]:
        satellites = self.__api_satellite_service__.find_all_by_category(category_id)
        satellites_favorite = self.find_all_is_favorite()

        list_sat = []
        for sat in satellites:
            list_sat.append(self.compare_satellites(sat, satellites_favorite))
        
        if (filter != None):
            return [sat for sat in list_sat if str(filter) in str(sat.id_provider)]
        
        return list_sat

    def find_all_is_favorite(self) -> list[Satellite]:
        return self.__satellite_repository__.find_all_is_favorite()

    def find_by_id_provider(self, id_provider: str) -> SatelliteWithPositionsModel:
        satellite = self.__api_satellite_service__.find_by_id(id_provider)
        satellites_favorite = self.find_all_is_favorite()

        if any(sat.id_provider == satellite.id_provider for sat in satellites_favorite):
            satellite.is_favorite = True
        else:
            satellite.is_favorite = False

        self.__satellite_service__.save_monitoring(satellite.id_provider)

        log = SatelliteLog()
        log.id_provider = satellite.id_provider
        log.name = satellite.name
        log.is_favorite = satellite.is_favorite
        log.time = datetime.datetime.now()

        self.__log_repository__.save(log)

        return satellite
    
    def compare_satellites(self, satellite: SatelliteWithPositionModel, satellites_favorite: list[Satellite]) -> SatelliteWithPositionModel:
        possible_satellite = None
        
        for sat in satellites_favorite:
            if (sat.name == satellite.name):
                possible_satellite = sat

        if possible_satellite != None:
            satellite.id = possible_satellite.id
            satellite.is_favorite = True
        else:
            satellite.is_favorite = False
        
        return satellite
    
    def find_trajectory(self) -> SatelliteTrajectory:
        id_satellite = self.__monitoring_repository__.find_first()

        if not id_satellite:
            return None
        
        satellite = self.__api_satellite_service__.find_by_id(id_satellite)

        return self.calculate_trajectory(satellite)
    
    def calculate_trajectory(self, satellite: SatelliteWithPositionsModel) -> SatelliteTrajectory:
        first_position = satellite.positions[0]
        last_position = satellite.positions[-1]

        timestamp_seconds = int(first_position.timestamp)
        time1 = datetime.utcfromtimestamp(timestamp_seconds)
        
        timestamp_seconds2 = int(last_position.timestamp)
        time2 = datetime.utcfromtimestamp(timestamp_seconds2)

        trajectory = SatelliteTrajectory()
        trajectory.azimuth = last_position.azimuth - first_position.azimuth
        trajectory.elevation = last_position.elevation - first_position.elevation
        trajectory.time = time2 - time1

        return trajectory
    
    def find_trajectory_log(self):
        return self.__log_repository__.find_all()



        
