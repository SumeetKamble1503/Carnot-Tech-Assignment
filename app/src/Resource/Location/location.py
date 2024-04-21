import json
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from flask import make_response, current_app as app
import traceback
import redis
from datetime import datetime
from src.Models import LatestLocationRequestModel, LatestLocationResponseModel
from src.Models import StartEndLocationRequestModel, StartEndLocationResponseModel
from src.Models import LocationPointsRequestModel, LocationPointsResponseModel, LocationPointModel

class LatestLocation(Resource):
    def __init__(self):
        self.redis_client = app.config['REDIS_CLIENT']
        
    def get(self,device_id):
        try:
            LatestLocationRequestModel(device_id=device_id)
            # Get the latest location data for the device from Redis
            # zrevrange funciton fetches 0,index element from the sorted set in descending order from the redis sorted set
            latest_location = self.redis_client.zrevrange(device_id, 0, 0, withscores=False)
            if latest_location:
                latest_location_data = json.loads(latest_location[0])
                latest_location_data['device_id'] = device_id
                return LatestLocationResponseModel(**latest_location_data).dict()
            else:
                return {"message": "No data found for the device"}, 400
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception:
            print(traceback.format_exc())
            return make_response("Error in Location API: Latest Location.", 500)
        

class StartEndLocation(Resource):
    def __init__(self):
        self.redis_client = app.config['REDIS_CLIENT']
    
    def get(self,device_id):
        try:
            StartEndLocationRequestModel(device_id=device_id)

            #Get the start and end locations for the device from Redis
            start_location = self.redis_client.zrange(device_id, 0, 0)
            end_location = self.redis_client.zrange(device_id, -1, -1)

            if start_location and end_location:
                start_location_data = json.loads(start_location[0])
                end_location_data = json.loads(end_location[0])

                response_data = {
                    "device_id": device_id,
                    "start_location": {
                        "location": start_location_data["location"],
                        "timestamp": start_location_data["timestamp"],
                        "speed": start_location_data["speed"]
                    },
                    "end_location": {
                        "location": end_location_data["location"],
                        "timestamp": end_location_data["timestamp"],
                        "speed": end_location_data["speed"]
                    }
                }
                return StartEndLocationResponseModel(**response_data).dict()
            else:
                return {"message": "No data found for the device"}, 404
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception:
            print(traceback.format_exc())
            return make_response("Error in Location API: Start End Location.", 500)
        
class LocationPoints(Resource):
    def __init__(self):
        self.redis_client = app.config['REDIS_CLIENT']
    
    def post(self,device_id):
        try:
            request_data = request.json
            # Check the request data
            LocationPointsRequestModel(device_id=device_id, start_time=request_data.get('start_time'), end_time=request_data.get('end_time'))
            
            start_time = request_data.get('start_time')
            end_time = request_data.get('end_time')

            # Convert start_time and end_time to datetime objects
            start_datetime = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
            end_datetime = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%SZ')
            
            # Get location points for the specified device ID within the specified time range
            location_points_json = self.redis_client.zrangebyscore(device_id, start_datetime.timestamp(), end_datetime.timestamp())

            if location_points_json:
                # Convert JSON strings back to Python dictionaries
                location_points = []
                for point_json in location_points_json:
                    point_data = json.loads(point_json)
                    new_point_data = {
                        'latitude': float(point_data['location'][0]),
                        'longitude': float(point_data['location'][1]),
                        'timestamp': point_data['timestamp']
                    }
                    location_points.append(LocationPointModel(**new_point_data))
                
                response_data = {
                    'device_id': device_id,
                    'location_points': location_points
                }
                
                return LocationPointsResponseModel(**response_data).dict(), 200
            else:
                return {'error': 'No location points found within the specified time range'}, 404
            
        except ValueError as e:
            return {'error': str(e)}, 400
        
        except Exception:
            print(traceback.format_exc())
            return make_response("Error in Location API: Location Points.", 500)