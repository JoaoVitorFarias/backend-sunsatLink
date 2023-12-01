from typing import Optional, Protocol, runtime_checkable

@runtime_checkable
class MonitoringRepository(Protocol):

    def save(self, id_satellite: str) -> None:
        ...

    def find_first(self) -> Optional[str]:
        ...