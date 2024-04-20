from pydantic import BaseModel
from typing import List

class LatestLocationResponseModel(BaseModel):
    device_id: str
    location: tuple
    timestamp: str
    speed: int

class LocationModel(BaseModel):
    location: tuple
    timestamp: str
    speed: int
class StartEndLocationResponseModel(BaseModel):
    device_id: str
    start_location: LocationModel
    end_location: LocationModel
    

class LocationPointModel(BaseModel):
    longitude: float
    latitude: float
    timestamp: str
    
class LocationPointsResponseModel(BaseModel):
    device_id: str
    location_points: List[LocationPointModel]

