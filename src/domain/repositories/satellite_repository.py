from domain.entities.satellite import Satellite
from typing import Optional, Protocol, runtime_checkable

@runtime_checkable
class SatelliteRepository(Protocol):
    def save(self, satellite: Satellite) -> Satellite:
        ...

    def delete(self, satellite: Satellite) -> None:
        ...

    def find_by_id(self, id_provider: str) -> Optional[Satellite]:
        ...

    def find_all_is_favorite(self) -> list[Satellite]:
        ...