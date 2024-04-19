import json
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from flask import make_response, current_app as app
import traceback
import redis
from datetime import datetime

class LatestLocation(Resource):
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='redis', port=6379, db=0)
        
    def get(self,device_id):
        try:
            # Get the latest location for the specified device ID
            latest_location = self.redis_client.zrevrange(f'device:{device_id}:locations', 0, 0, withscores=True)
            if latest_location:
                latest_location = latest_location[0]
                latitude, longitude, timestamp = latest_location[0].decode('utf-8').split(',')
                return {
                    'device_id': device_id,
                    'latitude': float(latitude),
                    'longitude': float(longitude),
                    'timestamp': timestamp
                }
            else:
                return {'error': 'Device ID not found'}, 404
        except:
            print(traceback.format_exc())
            return make_response("Error in Location API : Latest Location.", 500)
        

class StartEndLocation(Resource):
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='redis', port=6379, db=0)
    
    def get(self,device_id):
        try:
            # Get the start and end location for the specified device ID
            start_location = self.redis_client.zrange(f'device:{device_id}:locations', 0, 0)
            end_location = self.redis_client.zrange(f'device:{device_id}:locations', -1, -1)
            if start_location and end_location:
                start_latitude, start_longitude, start_timestamp = start_location[0].decode('utf-8').split(',')
                end_latitude, end_longitude, end_timestamp = end_location[0].decode('utf-8').split(',')
                return {
                    'device_id': device_id,
                    'start_location': {'latitude': float(start_latitude), 'longitude': float(start_longitude)},
                    'start_timestamp': start_timestamp,
                    'end_location': {'latitude': float(end_latitude), 'longitude': float(end_longitude)},
                    'end_timestamp': end_timestamp
                }
            else:
                return {'error': 'Device ID not found'}, 404
        except:
            print(traceback.format_exc())
            return make_response("Error in Location API : Start End Location.", 500)
        
class LocationPoints(Resource):
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='redis', port=6379, db=0)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('start_time', type=str, help='Start time (format: YYYY-MM-DDTHH:MM:SSZ)')
        self.parser.add_argument('end_time', type=str, help='End time (format: YYYY-MM-DDTHH:MM:%SSZ)')
    
    def get(self,device_id):
        try:
            # Get location points for the specified device ID within the specified time range
            args = self.parser.parse_args()
            start_time = args.get('start_time')
            end_time = args.get('end_time')

            # Check if start_time and end_time are provided
            if not (start_time and end_time):
                return {'error': 'Both start_time and end_time are required'}, 400

            # Convert start_time and end_time to datetime objects
            start_datetime = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
            end_datetime = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%SZ')

            if end_datetime <= start_datetime:
                return {'error': 'End time must be later than start time'}, 400
            
            # Get location points within the specified time range
            location_points = self.redis_client.zrangebyscore(f'device:{device_id}:locations', start_datetime.timestamp(), end_datetime.timestamp(), withscores=True)

            if location_points:
                # Extract latitude, longitude, and timestamp from each location point
                points = []
                for location in location_points:
                    latitude, longitude, timestamp = location[0].decode('utf-8').split(',')
                    points.append({
                        'latitude': float(latitude),
                        'longitude': float(longitude),
                        'timestamp': timestamp
                    })
                return {"response" : points}
            else:
                return {'error': 'No location points found within the specified time range'}, 404

        except ValueError as e:
            return {'error': str(e)}, 400