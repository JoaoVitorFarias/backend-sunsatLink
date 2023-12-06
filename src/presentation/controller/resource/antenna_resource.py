from pydantic import BaseModel
from typing import Optional

class AntennaPositionResource(BaseModel):
    id: Optional[str] = None
    latitude: float
    longitude: float
    altitude: float 
    azimuth: float
    elevation: float
