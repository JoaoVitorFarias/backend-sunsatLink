from domain.entities.position import Position
from domain.entities.satellite import Satellite

class SatelliteWithPositionsModel(Satellite):
    positions: list[Position]