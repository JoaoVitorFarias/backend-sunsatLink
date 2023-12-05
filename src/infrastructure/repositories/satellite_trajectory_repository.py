from domain.repositories import satellite_trajectory_repository
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Callable, Optional
from application.model.satellite_trajectory import SatelliteTrajectory

from infrastructure.repositories.db_model.satellite_trajectory_db import SatelliteTrajectoryDb

class SatelliteTrajectoryRepository:

  database: Callable[[], Session]

  def __init__(self, session = Callable[[], Session]):
    self.database = session
    
  def save(self, satellite_trajectory: SatelliteTrajectory) -> SatelliteTrajectory:
    
    satellite_trajectory_db = SatelliteTrajectoryDb()
    satellite_trajectory_db.azimuth = satellite_trajectory.azimuth
    satellite_trajectory_db.elevation = satellite_trajectory.elevation
    satellite_trajectory_db.movimentation_command = satellite_trajectory.movimentation_command
    satellite_trajectory_db.time = satellite_trajectory.time

    session = self.database()
    session.merge(satellite_trajectory_db)
    session.commit()

    return satellite_trajectory
  
  def find_last_antenna_by_command(self, command: int) -> Optional[SatelliteTrajectory]:
        session = self.database()
        data = session.query(SatelliteTrajectoryDb).filter(SatelliteTrajectoryDb.movimentation_command == command).first()
        if not data:
           return None
        
        trajectory = SatelliteTrajectory()
        trajectory.time = data.time
        trajectory.azimuth = data.azimuth
        trajectory.elevation = data.elevation
        trajectory.movimentation_command= data.movimentation_command
        
        return trajectory
  
  def find_first(self) -> Optional[SatelliteTrajectory]:
        session = self.database()
        data = session.query(SatelliteTrajectoryDb).order_by(desc(SatelliteTrajectoryDb.id)).first()
        trajectory = SatelliteTrajectory()
        trajectory.time = data.time
        trajectory.azimuth = data.azimuth
        trajectory.elevation = data.elevation
        trajectory.movimentation_command= data.movimentation_command
        
        return trajectory
  
  def delete(self) -> None:
    session = self.database()
    data = data = session.query(SatelliteTrajectoryDb).filter(SatelliteTrajectoryDb.movimentation_command == 1).first()

    if data is not None:
        session.delete(data)
        session.commit()

assert isinstance(SatelliteTrajectoryRepository({}), satellite_trajectory_repository.SatelliteTrajectoryRepository)