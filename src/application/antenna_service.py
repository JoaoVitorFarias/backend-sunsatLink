
from domain.entities.antenna_position import AntennaPosition
from domain.repositories.antenna_repository import AntennaRepository
import uuid

class AntennaService():
    __antenna_repository__: AntennaRepository

    def __init__(
        self,
        antenna_repository: AntennaRepository
    ):
        self.__antenna_repository__ = antenna_repository
        
    def save_position(self, antenna_position: AntennaPosition) -> AntennaPosition:
        antenna_position.id = uuid.uuid4().hex

        return self.__antenna_repository__.save_position(antenna_position)

    def find_position(self) -> list[AntennaPosition]:

        return self.__antenna_repository__.find_position()