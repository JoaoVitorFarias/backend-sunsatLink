from database import Base
from sqlalchemy import Column, String

class MonitoringDb(Base):
    __tablename__ = "monitoring"
    __table_args__ = {"extend_existing": True}

    id: str = Column(String(100), primary_key=True, nullable=False)
    id_satellite: str = Column(String(100), nullable=False)