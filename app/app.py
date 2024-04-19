import datetime
from flask import Flask, jsonify, request
import pandas as pd
import redis
from src.routes import create_routes
import json
from flask_restful import reqparse,Api
app = Flask(__name__)

# app = create_app()
BASE_PATH = '/api/v1/'

# CORS(app)
api = Api(app, BASE_PATH)
create_routes(api)


@app.route("/health-check")
def health_check():
    response = { "status": 200 , "data": "Success" }
    return jsonify(response)

@app.route('/transfer_data_test')
def transfer_data_test():
    try:
        import os
        # Get the current working directory
        current_directory = os.getcwd()

        # Define the relative path to the file from the current directory
        relative_path = 'assignment/raw_data (4) (6).csv'

        # Join the current directory with the relative path to get the absolute file path
        absolute_path = os.path.join(current_directory, relative_path)

        print(absolute_path)
        # return ({'message': 'Data transferred to Redis successfully!'})
        # Load Excel file into DataFrame
        df = pd.read_csv(absolute_path)

        # Sort DataFrame by device ID and time_stamp in descending order
        df_sorted = df.sort_values(by=['device_fk_id', 'sts'], ascending=[True, False])

        # Connect to Redis
        r = redis.StrictRedis(host='redis', port=6379, db=0)

        for _, row in df_sorted.iterrows():
            device_id = row['device_fk_id']
            timestamp = row['time_stamp']
            location = f"{row['latitude']},{row['longitude']},{timestamp}"
            # Store location data in Redis Sorted Set with key as device ID
            r.zadd(f'device:{device_id}:locations', {location: pd.Timestamp(timestamp).timestamp()})

        return {'message': 'Data transferred to Redis successfully!'}, 200
        # Iterate over sorted DataFrame and store latest data for each device ID in Redis
        for _, row in df_sorted.iterrows():
            device_id = row['device_fk_id']
            data = {
                'latitude': row['latitude'],
                'longitude': row['longitude'],
                'time_stamp': str(row['time_stamp']),
                'sts': str(row['sts']),
                'speed': row['speed']
            }
            # Store data in Redis hash with key as device ID
            serialized_data = json.dumps(data)
            if serialized_data is not None:
                # Store serialized data in Redis hash with key as device ID
                r.hset(f'device:{device_id}', 'latest_data', serialized_data)

        return ({'message': 'Data transferred to Redis successfully!'}), 200

    except Exception as e:
        print(str(e))
        return ({'error': str(e)}), 500
    

@app.route('/latest-device-info/<device_id>') 
def LatestDeviceInfo(device_id):
        r = redis.StrictRedis(host='redis', port=6379, db=0)
        # Get the latest location for the specified device ID
        latest_location = r.zrevrange(f'device:{device_id}:locations', 0, 0, withscores=True)
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
        

@app.route('/start-end-location/<device_id>')
def StartEndLocation(device_id):
        r = redis.StrictRedis(host='redis', port=6379, db=0)
        # Get the start and end location for the specified device ID
        start_location = r.zrange(f'device:{device_id}:locations', 0, 0)
        end_location = r.zrange(f'device:{device_id}:locations', -1, -1)
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
        
parser = reqparse.RequestParser()
parser.add_argument('start_time', type=str, help='Start time (format: YYYY-MM-DDTHH:MM:SSZ)')
parser.add_argument('end_time', type=str, help='End time (format: YYYY-MM-DDTHH:MM:%SSZ)')


@app.route('/location-points/<device_id>')
def LocationPoints(device_id):
        r = redis.StrictRedis(host='redis', port=6379, db=0)
        # Get location points for the specified device ID within the specified time range
        args = parser.parse_args()
        start_time = args.get('start_time')
        end_time = args.get('end_time')

        # Check if start_time and end_time are provided
        if not (start_time and end_time):
            return {'error': 'Both start_time and end_time are required'}, 400

        try:
            # Convert start_time and end_time to datetime objects
            start_datetime = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
            end_datetime = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%SZ')

            if end_datetime <= start_datetime:
                return {'error': 'End time must be later than start time'}, 400
            
            # Get location points within the specified time range
            location_points = r.zrangebyscore(f'device:{device_id}:locations', start_datetime.timestamp(), end_datetime.timestamp(), withscores=True)

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
