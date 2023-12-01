from domain.entities.position import Position
from presentation.controller.resource.satellite_resource import SatelliteResource

class SatelliteWithPositionsResource(SatelliteResource):
    positions: list[Position]