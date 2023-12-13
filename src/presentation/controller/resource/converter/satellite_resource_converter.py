import datetime
from application.model.satellite_log import SatelliteLog
from application.model.satellite_trajectory import SatelliteTrajectory
from application.model.satellite_with_position_model import SatelliteWithPositionModel
from application.model.satellite_with_positions_model import SatelliteWithPositionsModel
from domain.entities.satellite import Satellite
from presentation.controller.resource.satellite_log_resource import SatelliteLogResource
from presentation.controller.resource.satellite_resource import SatelliteResource
from presentation.controller.resource.satellite_trajectory_resource import SatelliteTrajectoryResource
from presentation.controller.resource.satellite_with_position_resource import SatelliteWithPositionResource
from presentation.controller.resource.satellite_with_positions_resource import SatelliteWithPositionsResource

def convertToSatelliteResource(satellite: Satellite):
    return SatelliteResource(
        id=satellite.id,
        name=satellite.name,
        is_favorite=satellite.is_favorite,
        id_provider=str(satellite.id_provider)
    )

def convertToSatelliteWithPositionResource(satellite: SatelliteWithPositionModel):
    return SatelliteWithPositionResource(
        id = satellite.id if hasattr(satellite, 'id') else None,
        name = satellite.name,
        is_favorite = satellite.is_favorite,
        id_provider = str(satellite.id_provider),
        longitude = satellite.longitude,
        latitude = satellite.latitude,
        altitude = satellite.altitude
    )

def convertToSatelliteWithPositionsResource(satellite: SatelliteWithPositionsModel):
    return SatelliteWithPositionsResource(
        id = satellite.id if hasattr(satellite, 'id') else None,
        name = satellite.name,
        is_favorite = satellite.is_favorite,
        id_provider = str(satellite.id_provider),
        positions = satellite.positions
    )

def convertToSatellite(resource: SatelliteResource):
    data = Satellite()

    data.id = resource.id
    data.name = resource.name
    data.is_favorite = resource.is_favorite
    data.id_provider = str(resource.id_provider)

    return data

def convertToSatelliteTrajectoryResource(satellite: SatelliteTrajectory):
    if (satellite.movimentation_command == 1):
        time = 90
    elif (satellite.movimentation_command == 2):
        time = int(satellite.time.total_seconds())
    else: 
        time = satellite.time

    return SatelliteTrajectoryResource(
        time=  time,
        azimuth= satellite.azimuth,
        elevation= satellite.elevation,
        movimentationCommand = satellite.movimentation_command
    )

def convertToSatelliteLog(resource: SatelliteLog):
    data = SatelliteLogResource(
        id = resource.id,
        name = resource.name,
        is_favorite = resource.is_favorite,
        id_provider = str(resource.id_provider),
        time = resource.time
    )

    return data