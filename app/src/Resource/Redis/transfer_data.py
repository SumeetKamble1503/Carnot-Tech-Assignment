from flask import jsonify
import Resource
import pandas as pd
import redis

class TransferData(Resource):
    def get(self):
        try:
            # Load Excel file into DataFrame
            df = pd.read_excel('./assignment/raw_data (4) (6).csv')

            # Sort DataFrame by device ID and time_stamp in descending order
            df_sorted = df.sort_values(by=['device_fk_id', 'time_stamp'], ascending=[True, False])

            # Connect to Redis
            r = redis.StrictRedis(host='localhost', port=6379, db=0)

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
                r.hmset(f'device:{device_id}', data)

            return jsonify({'message': 'Data transferred to Redis successfully!'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
class DeleteData(Resource):
    def delete(self):
        try:
            # Connect to Redis
            r = redis.StrictRedis(host='localhost', port=6379, db=0)

            # Delete all keys from Redis
            r.flushdb()

            return jsonify({'message': 'All data deleted from Redis successfully!'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500