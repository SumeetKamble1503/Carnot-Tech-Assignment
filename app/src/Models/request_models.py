from pydantic import BaseModel, validator
from datetime import datetime

class LatestLocationRequestModel(BaseModel):
    device_id: str

    @validator('device_id')
    def device_id_numeric(cls, v):
        if not v.isnumeric():
            raise ValueError('Device ID must be numeric')
        return v
    
class StartEndLocationRequestModel(BaseModel):
    device_id: str

    @validator('device_id')
    def device_id_numeric(cls, v):
        if not v.isnumeric():
            raise ValueError('Device ID must be numeric')
        return v

class LocationPointsRequestModel(BaseModel):
    device_id: str
    start_time: str
    end_time: str

    @validator('device_id')
    def device_id_numeric(cls, v):
        if not v.isnumeric():
            raise ValueError('Device ID must be numeric')
        return v
    
    # Validate start_time and end_time format
    @validator('start_time', 'end_time')
    def validate_datetime(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            raise ValueError('Invalid datetime format. Use the format: YYYY-MM-DDTHH:MM:SSZ')
        return v
    
    # Validate that end_time is later than start_time
    @validator('end_time')
    def validate_end_time(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('End time must be later than start time')
        return v
    
    
    
