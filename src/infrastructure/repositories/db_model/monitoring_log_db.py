import datetime
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum
from database import Base
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy import Column, Enum as EnumDB

class MonitoringLogDb(Base):
    __tablename__ = "monitoring_log"
    __table_args__ = {"extend_existing": True}

    id: str = Column(String(100), primary_key=True, nullable=False)
    name: str = Column(String(100), nullable=False)
    is_favorite: bool = Column(Boolean, default=True)
    id_provider: str = Column(String(100), nullable=False)
    time: datetime = Column(DateTime, nullable=False)