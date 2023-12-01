from datetime import timedelta
from pydantic import BaseModel

class SatelliteTrajectoryResource(BaseModel):
    time: timedelta
    azimuth: float
    elevation: float