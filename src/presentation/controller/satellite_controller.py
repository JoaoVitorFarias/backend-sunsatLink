from fastapi import APIRouter, status, HTTPException, Query
from presentation.controller.resource.converter.satellite_resource_converter import convertToSatellite, convertToSatelliteLog, convertToSatelliteResource, convertToSatelliteTrajectoryResource, convertToSatelliteWithPositionResource, convertToSatelliteWithPositionsResource
from presentation.controller.resource.satellite_resource import SatelliteResource
from database import engine, Base
from presentation.controller import satellite_query_service, satellite_service

Base.metadata.create_all(bind=engine)

router_satellite = APIRouter(
    prefix="/satellite",
    tags=["satellite"],
    responses={404: {"description": "Not found"}},
)

@router_satellite.get("/{category_id}") 
def get_all_by_category(category_id: str,
                        filter: str = None,
                        page: int = Query(1, alias="page"), 
                        offset: int = Query(10, alias="offset")):
    skip = (page - 1) * offset
    limit = skip + offset
    satellites = satellite_query_service.find_all_by_category(category_id, filter)

    return list(map(lambda sat: convertToSatelliteWithPositionResource(sat), satellites))[skip:limit]

@router_satellite.get("/favorite/")
def get_all_favorite(page: int = Query(1, alias="page"), offset: int = Query(10, alias="offset")):
    skip = (page - 1) * offset
    limit = skip + offset
    satellites = satellite_query_service.find_all_is_favorite()

    return list(map(lambda sat: convertToSatelliteResource(sat), satellites))[skip:limit]

@router_satellite.get("/provider/{id_provider}/{movimentation_command}")
def get_by_id(id_provider: str, movimentation_command: int):
    satellite = satellite_query_service.find_by_id_provider(id_provider, movimentation_command)

    if not satellite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  detail = "Satellite not found"
        )
    
    return convertToSatelliteWithPositionsResource(satellite)


@router_satellite.get("/monitoring/")
def get_monitoring_operation():
    trajectory = satellite_query_service.find_trajectory()

    if not trajectory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  detail = "Trajectory not found"
        )
    
    return convertToSatelliteTrajectoryResource(trajectory)

@router_satellite.post("/")
def save(request: SatelliteResource):
    satellite = satellite_service.save(convertToSatellite(request))

    return convertToSatelliteResource(satellite)

@router_satellite.delete("/")
def delete(request: SatelliteResource):
    satellite_service.delete(convertToSatellite(request))

@router_satellite.get("/monitoring/log/")
def get_monitoring_log(
                    page: int = Query(1, alias="page"), 
                    offset: int = Query(10, alias="offset")):
    skip = (page - 1) * offset
    limit = skip + offset
    log = satellite_query_service.find_trajectory_log()

    if not log:
        return log
    
    return list(map(lambda sat: convertToSatelliteLog(sat), log))[skip:limit]


@router_satellite.get("/positions/{id_provider}")
def get_positions(id_provider: str):
    positions = satellite_query_service.find_positions(id_provider)
    
    return positions
