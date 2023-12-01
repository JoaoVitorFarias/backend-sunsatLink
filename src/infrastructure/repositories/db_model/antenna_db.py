from sqlalchemy.ext.declarative import declarative_base
from enum import Enum
from database import Base
from sqlalchemy import Column, String, Boolean, Numeric
from sqlalchemy import Column, Enum as EnumDB

class AntennaDb(Base):
    __tablename__ = "antenna"
    __table_args__ = {"extend_existing": True}

    id: str = Column(String(100), primary_key=True, nullable=False)
    latitude = Column(Numeric, nullable=False)
    longitude = Column(Numeric, nullable=False)
    altitude  = Column(Numeric, nullable=False)
    azimuth = Column(Numeric, nullable=False)
    elevation = Column(Numeric, nullable=False)

