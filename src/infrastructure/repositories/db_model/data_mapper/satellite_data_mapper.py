from domain.entities.satellite import Satellite
from infrastructure.repositories.db_model.satellite_db import SatelliteDb

def map_to_satellite(source: SatelliteDb) -> Satellite:
    satellite = Satellite()

    satellite.id = source.id
    satellite.name = source.name
    satellite.is_favorite = source.is_favorite
    satellite.id_provider = source.id_provider

    return satellite

def map_from_satellite(source: Satellite) -> SatelliteDb:
    satellite = SatelliteDb()

    satellite.id = source.id
    satellite.name = source.name
    satellite.is_favorite = source.is_favorite
    satellite.id_provider = source.id_provider

    return satellite