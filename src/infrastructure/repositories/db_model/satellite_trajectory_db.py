from database import Base
from sqlalchemy import Column, DateTime, Numeric, Integer

class SatelliteTrajectoryDb(Base):
    __tablename__ = "satellite_trajectory"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    time = Column(Numeric, nullable=False)
    azimuth = Column(Numeric, nullable=False)
    elevation = Column(Numeric, nullable=False)
    movimentation_command = Column(Numeric, nullable=True)

