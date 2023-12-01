from typing import Protocol, runtime_checkable
from application.model.satellite_with_position_model import SatelliteWithPositionModel
from application.model.satellite_with_positions_model import SatelliteWithPositionsModel


@runtime_checkable
class ApiSatelliteService(Protocol):

    def find_all_by_category(self, category_id: str, latitude="-15.779528", longitude="-47.929686", altitude="0", search_radius="90") -> list[SatelliteWithPositionModel]:
        ...

    def find_by_id(self, id_provider: str, latitude="-15.779528", longitude="-47.929686", altitude="0", seconds="300") -> SatelliteWithPositionsModel:
        ...