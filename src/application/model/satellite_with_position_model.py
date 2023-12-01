from domain.entities.satellite import Satellite

class SatelliteWithPositionModel(Satellite):
    latitude: float
    longitude: float
    altitude: float