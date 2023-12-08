import uuid
from domain.entities.antenna_position import AntennaPosition
from domain.repositories.antenna_repository import AntennaRepository as BaseRepository
from sqlalchemy.orm import Session
from typing import Callable, Optional
from infrastructure.repositories.db_model.antenna_db import AntennaDb

class AntennaRepository:
    
    database: Callable[[], Session]

    def __init__(self, session = Callable[[], Session]):
        self.database = session

    def save_position(self, antenna_position: AntennaPosition) -> AntennaPosition:
        antenna_db = AntennaDb()
        antenna_db.id = antenna_position.id
        antenna_db.latitude = antenna_position.latitude
        antenna_db.altitude = antenna_position.altitude
        antenna_db.longitude = antenna_position.longitude
        antenna_db.azimuth = antenna_position.azimuth
        antenna_db.elevation = antenna_position.elevation

        session = self.database()
        antennaUpdated = session.merge(antenna_db)
        session.commit()


        antenna = AntennaPosition(
            id = antennaUpdated.id,
            latitude = antennaUpdated.latitude,
            altitude = antennaUpdated.altitude,
            longitude = antennaUpdated.longitude,
            azimuth = antennaUpdated.azimuth,
            elevation = antennaUpdated.elevation
        )
        
        return antenna

    def find_position(self) -> list[AntennaPosition]:
        session = self.database()
        data = session.query(AntennaDb).order_by(AntennaDb.created_at.desc()).all()

        list_data = []
        for pos in data:
            antenna = AntennaPosition(
                id = pos.id,
                latitude = pos.latitude,
                altitude = pos.altitude,
                longitude = pos.longitude,
                azimuth = pos.azimuth,
                elevation = pos.elevation
            )
            list_data.append(antenna)

        return list_data
    
    def find_first(self) -> Optional[AntennaPosition]:
        session = self.database()
        data = session.query(AntennaDb).order_by(AntennaDb.created_at.desc()).first()
        if not data:
            return None
        
        antenna = AntennaPosition(
            id = data.id,
            latitude = data.latitude,
            altitude = data.altitude,
            longitude = data.longitude,
            azimuth = data.azimuth,
            elevation = data.elevation
        )
        return antenna

assert isinstance(AntennaRepository(
    {}), BaseRepository)
