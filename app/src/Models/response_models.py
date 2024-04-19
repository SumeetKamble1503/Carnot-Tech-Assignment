from pydantic import BaseModel
from typing import List

class LatestLocationResponseModel(BaseModel):
    device_id: str
    latitude: float
    longitude: float
    timestamp: str

class StartEndLocationResponseModel(BaseModel):
    device_id: str
    start_location: dict
    start_timestamp: str
    end_location: dict
    end_timestamp: str

class LocationPointsResponseModel(BaseModel):
    response: List[dict]

