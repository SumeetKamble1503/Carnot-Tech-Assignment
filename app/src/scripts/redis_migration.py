
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

from flask import Flask
import pandas as pd
import redis

app = Flask(__name__)

class RedisDataMigration():
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def migrate(self):
            
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

            return ({'message': 'Data transferred to Redis successfully!'}), 200

        except Exception as e:
            print("SK")
            print(str(e))
            return ({'error': str(e)}), 500
        
if __name__ == "__main__":
    obj = RedisDataMigration()
    obj.migrate()

