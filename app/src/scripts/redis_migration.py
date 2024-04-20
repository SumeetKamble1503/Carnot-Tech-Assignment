
# from flask import Flask
# import pandas as pd
# import redis

# '''

#     This script will migrate all the marketing_list from marketing_contacts collection to contact_list collection.
    
#     Commands to run this script
#     1. docker-compose -f docker-compose.yml exec backend bash
#     2. python3 src/scripts/redis_migration.py

# '''


# app = Flask(__name__)

# class RedisDataMigration():
#     def __init__(self):
#         self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

#     def migrate(self):
#         try:
#             # Load Excel file into DataFrame
#             df = pd.read_excel('./assignment/raw_data (4) (6).csv')

#             # Sort DataFrame by device ID and time_stamp in descending order
#             df_sorted = df.sort_values(by=['device_fk_id', 'time_stamp'], ascending=[True, False])

#             # Connect to Redis
#             # self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

#             # Iterate over sorted DataFrame and store latest data for each device ID in Redis
#             for _, row in df_sorted.iterrows():         
#                 device_id = row['device_fk_id']
#                 data = {
#                     'latitude': row['latitude'],
#                     'longitude': row['longitude'],
#                     'time_stamp': str(row['time_stamp']),
#                     'sts': str(row['sts']),
#                     'speed': row['speed']
#                 }
#                 # Store data in Redis hash with key as device ID
#                 self.redis_client.hmset(f'device:{device_id}', data)

#             # if self.redis_client is not None:
#             #     self.redis_client.close()
#             self.redis_client.connection_pool.disconnect()

#             print('Data transferred to Redis successfully!')

#         except Exception as e:
#             return ({'error': str(e)}), 500


# if __name__ == "__main__":
#     obj = RedisDataMigration()
#     print(obj)
#     obj.migrate()

from flask import Flask,current_app as my_app
import pandas as pd
import redis

app = Flask(__name__)

class RedisDataMigration():
    def __init__(self):
        self.redis_client = redis.Redis(host='redis', port=6379, db=0)

    def migrate(self):
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

            for _, row in df_sorted.iterrows():
                device_id = row['device_fk_id']
                timestamp = row['time_stamp']
                location = f"{row['latitude']},{row['longitude']},{timestamp}"
                # Store location data in Redis Sorted Set with key as device ID
                self.redis_client.zadd(f'device:{device_id}:locations', {location: pd.Timestamp(timestamp).timestamp()})
            self.redis_client.connection_pool.disconnect()
            return {'message': 'Data transferred to Redis successfully!'}, 200
        except Exception as e:
            return {'error': str(e)}, 500
        
if __name__ == "__main__":
    obj = RedisDataMigration()
    obj.migrate()

