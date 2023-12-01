from application.user_service import UserService
from infrastructure.repositories.monitoring_log_repository import MonitoringLogRepository
from infrastructure.repositories.monitoring_repository import MonitoringRepository
from infrastructure.repositories.tokens_repository import TokensRepository
from infrastructure.repositories.user_repository import UserRepository
from application.satellite_query_service import SatelliteQueryService
from application.satellite_service import SatelliteService
from application.antenna_service import AntennaService
from infrastructure.repositories.satellite_repository import SatelliteRepository
from infrastructure.repositories.antenna_repository import AntennaRepository
from database import SessionLocal
from infrastructure.service.n2yo_satellite_service import N2yoSatelliteService

databaseSessionGenerator = SessionLocal

userRepository = UserRepository(databaseSessionGenerator)
tokensRepository = TokensRepository()
userService = UserService(
    usersRepository = userRepository,
    tokensRepository=tokensRepository
)
satellite_repository = SatelliteRepository(databaseSessionGenerator)
monitoring_repository = MonitoringRepository(databaseSessionGenerator)
log_repository = MonitoringLogRepository(databaseSessionGenerator)
api_satellite_service = N2yoSatelliteService()
antenna_repository = AntennaRepository(databaseSessionGenerator)
antenna_service = AntennaService(antenna_repository)
satellite_service = SatelliteService(satellite_repository, monitoring_repository, log_repository)
satellite_query_service = SatelliteQueryService(satellite_repository,
                                                api_satellite_service,
                                                monitoring_repository,
                                                satellite_service,
                                                log_repository)
