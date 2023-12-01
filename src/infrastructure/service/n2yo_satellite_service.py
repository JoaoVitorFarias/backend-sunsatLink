import datetime
from application.api_satellite_service import ApiSatelliteService
import requests
from application.model.satellite_with_position_model import SatelliteWithPositionModel

from application.model.satellite_with_positions_model import SatelliteWithPositionsModel
from domain.entities.position import Position

class N2yoSatelliteService: 
    URL = "https://api.n2yo.com/rest/v1/satellite"
    API_KEY = "DA7W8Q-M7NNDG-6PYH2P-5543"
    PARAMS = {'apiKey':API_KEY}

    def __init__(self):
        pass

    def find_all_by_category(self, category_id: str, latitude="-15.779528", longitude="-47.929686", altitude="0", search_radius="90") -> list[SatelliteWithPositionModel]:
        complementary_url = f"/above/{latitude}/{longitude}/{altitude}/{search_radius}/{category_id}"
        response = requests.get(url = self.URL + complementary_url, params = self.PARAMS)

        satellites = self.mapToSatelliteWithPositionModel(response)

        return satellites

    def find_by_id(self, id_provider: str, latitude="-15.779528", longitude="-47.929686", altitude="0", seconds="300") -> SatelliteWithPositionsModel:
        complementary_url = f"/positions/{id_provider}/{latitude}/{longitude}/{altitude}/{seconds}"
        response = requests.get(url = self.URL + complementary_url, params = self.PARAMS)

        return self.mapToSatelliteWithPositionsModel(response, seconds)
    
    def mapToSatelliteWithPositionsModel(self, response, seconds) -> SatelliteWithPositionsModel:
        data = response.json()
        satellite = SatelliteWithPositionsModel()
        satellite.name = data['info']['satname']
        satellite.id_provider = data['info']['satid']
        positions = []

        for i in range(300):
            positions.append(Position(
                latitude = data['positions'][i]['satlatitude'],
                longitude = data['positions'][i]['satlongitude'],
                altitude = data['positions'][i]['sataltitude'],
                azimuth = data['positions'][i]['azimuth'],
                elevation = data['positions'][i]['elevation'],
                ra = data['positions'][i]['ra'],
                dec = data['positions'][i]['dec'],
                timestamp = data['positions'][i]['timestamp']
            ))
        
        satellite.positions = positions
        return satellite
    
    def mapToSatelliteWithPositionModel(self, response) -> list[SatelliteWithPositionModel]:
        data = response.json()
        satellites = []
        
        for sat in data['above']:
            satellite = SatelliteWithPositionModel()
            satellite.id_provider = sat['satid']
            satellite.name = sat['satname']
            satellite.latitude = sat['satlat']
            satellite.longitude = sat['satlng']
            satellite.altitude = sat['satalt']
            
            satellites.append(satellite)

        return satellites