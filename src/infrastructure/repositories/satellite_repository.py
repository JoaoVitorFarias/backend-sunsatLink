from domain.entities.satellite import Satellite
from domain.repositories import satellite_repository
from sqlalchemy.orm import Session
from typing import Callable, Optional
from infrastructure.repositories.db_model.data_mapper.satellite_data_mapper import map_from_satellite, map_to_satellite

from infrastructure.repositories.db_model.satellite_db import SatelliteDb

class SatelliteRepository:

    database: Callable[[], Session]

    def __init__(self, session = Callable[[], Session]):
        self.database = session
    
    def save(self, satellite: Satellite) -> Satellite:
        session = self.database()
        satellite_db = map_from_satellite(satellite)
        session.merge(satellite_db)
        session.commit()

        return map_to_satellite(satellite_db)
    
    def delete(self, satellite: Satellite) -> None:
        session = self.database()
        data = data = session.query(SatelliteDb).filter(SatelliteDb.id == satellite.id).first()

        if data is not None:
            session.delete(data)
            session.commit()

    def find_by_id(self, id_provider: str) -> Optional[Satellite]:
        session = self.database()
        data = session.query(SatelliteDb).filter(SatelliteDb.id_provider == id_provider).first()
        
        return map_to_satellite(data)

    def find_all_is_favorite(self) -> list[Satellite]:
        session = self.database()
        data = session.query(SatelliteDb).filter(SatelliteDb.is_favorite == True).all()
        
        list_data = []
        for sat in data:
            list_data.append(map_to_satellite(sat))

        return list_data

assert isinstance(SatelliteRepository(
    {}), satellite_repository.SatelliteRepository)