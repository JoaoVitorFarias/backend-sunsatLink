from presentation.controller.resource.satellite_resource import SatelliteResource

class SatelliteWithPositionResource(SatelliteResource):
    latitude: float
    longitude: float
    altitude: float