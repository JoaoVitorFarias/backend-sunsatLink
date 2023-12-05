from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class SatelliteTrajectory(BaseModel):
  time: Optional[datetime]
  elevation: float
  movimentation_command: int
  azimuth: float