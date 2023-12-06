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
from domain.repositories.satellite_trajectory_repository import SatelliteTrajectoryRepository
from src.domain.repositories.antenna_repository import AntennaRepository

class SatelliteQueryService():
    __satellite_repository__: SatelliteRepository
    __api_satellite_service__: ApiSatelliteService
    __monitoring_repository__: MonitoringRepository
    __satellite_service__: SatelliteService 
    __log_repository__: MonitoringLogRepository
    __satellite_trajectory_repository__: SatelliteTrajectoryRepository
    __antenna_repository__: AntennaRepository

    def __init__(
        self,
        satellite_repository: SatelliteRepository,
        api_satellite_service: ApiSatelliteService,
        monitoring_repository: MonitoringRepository,
        satellite_service: SatelliteService,
        log_repository: MonitoringLogRepository,
        satellite_trajectory_repository: SatelliteTrajectoryRepository,
        antenna_repository: AntennaRepository
    ):
        self.__satellite_repository__ = satellite_repository
        self.__api_satellite_service__ = api_satellite_service
        self.__monitoring_repository__ = monitoring_repository
        self.__satellite_service__ = satellite_service
        self.__log_repository__ = log_repository
        self.__satellite_trajectory_repository__ = satellite_trajectory_repository
        self.__antenna_repository__ = antenna_repository


    def find_all_by_category(self, category_id: str, filter=None) -> list[SatelliteWithPositionModel]:
        satellites = self.__api_satellite_service__.find_all_by_category(category_id)
        satellites_favorite = self.find_all_is_favorite()
        list_sat = []

        if not satellites:
            return list_sat
        
        for sat in satellites:
            list_sat.append(self.compare_satellites(sat, satellites_favorite))
        
        if (filter != None):
            return [sat for sat in list_sat if (str(filter) in str(sat.id_provider)) or (str(filter) in str(sat.name)) ]
        
        return list_sat

    def find_all_is_favorite(self) -> list[Satellite]:
        return self.__satellite_repository__.find_all_is_favorite()

    def find_by_id_provider(self, id_provider: str, movimentation_command: int) -> SatelliteWithPositionsModel:
        antenna = self.__antenna_repository__.find_first()
        if not antenna:
            satellite = self.__api_satellite_service__.find_by_id(id_provider)
        else: 
            satellite = self.__api_satellite_service__.find_by_id(id_provider, antenna.latitude, antenna.longitude, antenna.altitude)

        satellites_favorite = self.find_all_is_favorite()

        if any(sat.id_provider == satellite.id_provider for sat in satellites_favorite):
            satellite.is_favorite = True
        else:
            satellite.is_favorite = False

        self.__satellite_service__.save_monitoring(satellite.id_provider)

        '''trajectory = SatelliteTrajectory()
        trajectory.azimuth = 0.0
        trajectory.elevation = 0.0
        trajectory.time = datetime.now()
        trajectory.movimentation_command = movimentation_command

        self.__satellite_trajectory_repository__.save(trajectory)'''

        self.resolve_trajectory(movimentation_command)

        log = SatelliteLog()
        log.id_provider = satellite.id_provider
        log.name = satellite.name
        log.is_favorite = satellite.is_favorite
        log.time = datetime.now()

        
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
    
    def find_trajectory(self):
        return self.__satellite_trajectory_repository__.find_first()

    
    def resolve_trajectory(self, movimentation_command: str) -> SatelliteTrajectory | None:
        id_satellite = self.__monitoring_repository__.find_first()

        if not id_satellite:
            return None
        
        antenna = self.__antenna_repository__.find_first()
        if not antenna:
            satellite = self.__api_satellite_service__.find_by_id(id_satellite)
        else: 
            satellite = self.__api_satellite_service__.find_by_id(id_satellite, antenna.latitude, antenna.longitude, antenna.altitude)

        trajectory = SatelliteTrajectory()

        if (movimentation_command == 0):
          return self.stop_position(satellite, trajectory)
        elif(movimentation_command == 1):
          return self.start_position(satellite, trajectory)
        else: # trajectory.movimentation_command == 2
          return self.calculate_trajectory(satellite, trajectory)
    
    def stop_position(self, satellite: SatelliteWithPositionsModel, trajectory: SatelliteTrajectory) -> SatelliteTrajectory:
        self.__satellite_trajectory_repository__.delete()
        trajectory.azimuth = 0.0
        trajectory.elevation = 0.0
        trajectory.movimentation_command = 0
        trajectory.time = 0

        self.__satellite_trajectory_repository__.save(trajectory)

        return trajectory

    def start_position(self, satellite: SatelliteWithPositionsModel, trajectory: SatelliteTrajectory) -> SatelliteTrajectory:
        # verificar se chegou na posicao esperada e se chegou colocar o movimentario para 2.
        initial_trajectory = self.__satellite_trajectory_repository__.find_last_antenna_by_command(1)
        antenna = self.__antenna_repository__.find_first()
       
        position = satellite.positions[0]

        if initial_trajectory:
            if (((int(initial_trajectory.azimuth) - 3) >= int(position.azimuth) and (int(initial_trajectory.azimuth) + 3) <= int(position.azimuth))
            and ((int(initial_trajectory.elevation) - 3) >= int(self.calculate_elevation(position.elevation)) and (int(initial_trajectory.elevation) + 3) <= int(self.calculate_elevation(position.elevation)))):
                self.__satellite_trajectory_repository__.delete()
                return self.calculate_trajectory(satellite, trajectory)
                   
        else:
            if not antenna:
                trajectory.azimuth = position.azimuth
                trajectory.elevation = self.calculate_elevation(position.elevation)
                trajectory.time = int((datetime.utcfromtimestamp(int(position.timestamp))- datetime.now()).total_seconds())
                trajectory.movimentation_command = 1

                self.__satellite_trajectory_repository__.save(trajectory)

                return trajectory
            else: 
                trajectory.azimuth = self.calculate_azimuth(antenna.azimuth, position.azimuth)
                trajectory.elevation = self.calculate_elevation(position.elevation) - self.calculate_elevation(antenna.elevation)
                trajectory.time = int((datetime.utcfromtimestamp(int(position.timestamp))- datetime.now()).total_seconds())
                trajectory.movimentation_command = 1

                self.__satellite_trajectory_repository__.save(trajectory)

                return trajectory
    
    def calculate_trajectory(self, satellite: SatelliteWithPositionsModel, trajectory: SatelliteTrajectory) -> SatelliteTrajectory:
        first_position = satellite.positions[0]
        last_position = satellite.positions[-1]

        timestamp_seconds = int(first_position.timestamp)
        time1 = datetime.utcfromtimestamp(timestamp_seconds)
        
        timestamp_seconds2 = int(last_position.timestamp)
        time2 = datetime.utcfromtimestamp(timestamp_seconds2)

        trajectory.azimuth = self.calculate_azimuth(first_position.azimuth, last_position.azimuth)

        trajectory.elevation = self.calculate_elevation(last_position.elevation) - self.calculate_elevation(first_position.elevation)
        trajectory.time = int((time2 - time1).total_seconds())
        trajectory.movimentation_command = 2

        self.__satellite_trajectory_repository__.save(trajectory)
        trajectory.time = time2 - time1

        return trajectory
    
    def find_trajectory_log(self):
        satellites_favorite = self.find_all_is_favorite()
        logs =  self.__log_repository__.find_all()

        if not logs:
            logs
        
        list_sat = []
        for sat in logs:
            list_sat.append(self.compare_satellites(sat, satellites_favorite))
        
        return list_sat

    
    def calculate_elevation(self, x): 
        elevation = ((-0.0019*(x**2)) + (-0.5126*x) + (26.429)) * 360

        if (elevation > 16200 or elevation < -16200):
            return 0
        
        return elevation
    
    def find_positions(self, id_provider: str):
        antenna = self.__antenna_repository__.find_first()
        if not antenna:
            satellite = self.__api_satellite_service__.find_by_id(id_provider)
        else: 
            satellite = self.__api_satellite_service__.find_by_id(id_provider, antenna.latitude, antenna.longitude, antenna.altitude)

        return satellite.positions
    
    def calculate_azimuth(self, a, b):
        delta = abs(b - a)

        menor_distancia = min(delta, 360-delta)
        if delta <= 180:
            if b > a:
                return menor_distancia
            else:
                return -menor_distancia
        else:
            if b > a:
                return -menor_distancia
            else:
                return menor_distancia
