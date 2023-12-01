from typing import Optional
from pydantic import BaseModel

class AntennaPosition(BaseModel):
    id: Optional[str]
    latitude: float
    longitude: float
    altitude: float 
    azimuth: float
    elevation: float
