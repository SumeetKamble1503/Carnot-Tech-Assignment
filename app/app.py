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
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
