from datetime import timedelta
from pydantic import BaseModel

class SatelliteTrajectoryResource(BaseModel):
    time: int
    azimuth: float
    elevation: float