from domain.entities.antenna_position import AntennaPosition
from typing import Optional, Protocol, runtime_checkable

@runtime_checkable
class AntennaRepository(Protocol):
    def save_position(self, antenna_position: AntennaPosition) -> AntennaPosition:
        ...

    def find_position(self) -> list[AntennaPosition]:
        ...
    
    def find_first(self) -> Optional[AntennaPosition]:
        ...