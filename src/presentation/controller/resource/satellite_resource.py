from pydantic import BaseModel
from typing import Optional

class SatelliteResource(BaseModel):
    id: Optional[str]
    name: str
    is_favorite: bool
    id_provider: str