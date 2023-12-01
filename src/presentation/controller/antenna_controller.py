from domain.entities.antenna_position import AntennaPosition
from fastapi import APIRouter, status, HTTPException, Query
from presentation.controller.resource.antenna_resource import AntennaPositionResource
from database import engine, Base
from presentation.controller import antenna_service

Base.metadata.create_all(bind=engine)

router_antenna = APIRouter(
    prefix="/antenna",
    tags=["antenna"],
    responses={404: {"description": "Not found"}},
)

@router_antenna.post("/position/")
def save_position(request: AntennaPositionResource):
    antenna_position= AntennaPosition(
        altitude = request.altitude,
        azimuth = request.azimuth,
        elevation = request.elevation,
        latitude = request.latitude,
        longitude = request.longitude
    )
    

    saved_position = antenna_service.save_position(antenna_position)
    
    return saved_position

@router_antenna.get("/position/")
def get_position(page: int = Query(1, alias="page"), 
                offset: int = Query(10, alias="offset")):
    skip = (page - 1) * offset
    limit = skip + offset
    positions = antenna_service.find_position()

    list_positions = []

    for pos in positions:
        antenna = AntennaPositionResource(
            id = pos.id,
            latitude = pos.latitude,
            altitude = pos.altitude,
            longitude = pos.longitude,
            azimuth = pos.azimuth,
            elevation = pos.elevation
        )
        list_positions.append(antenna)

    return list_positions[skip:limit]


