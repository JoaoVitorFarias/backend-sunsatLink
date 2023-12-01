from typing import Protocol, runtime_checkable

from application.model.satellite_log import SatelliteLog

@runtime_checkable
class MonitoringLogRepository(Protocol):

    def save(self, log: SatelliteLog) -> None:
        ...

    def find_all(self) -> list[SatelliteLog]:
        ...