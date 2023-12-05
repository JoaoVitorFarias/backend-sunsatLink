from application.model.satellite_trajectory import SatelliteTrajectory
from typing import Optional, Protocol, runtime_checkable

@runtime_checkable
class SatelliteTrajectoryRepository(Protocol):
    def save(self, satellite_trajectory: SatelliteTrajectory) -> SatelliteTrajectory:
        ...
    
    def find_last_antenna_by_command(self, command: int) -> Optional[SatelliteTrajectory]:
        ...

    def find_first(self) -> Optional[SatelliteTrajectory]:
        ...
    
    def delete(self) -> None:
        ...