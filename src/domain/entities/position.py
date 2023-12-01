from pydantic import BaseModel

class Position(BaseModel):
    latitude: float
    longitude: float
    altitude: float 
    azimuth: float
    elevation: float
    ra: float   
    dec: float
    timestamp: str
