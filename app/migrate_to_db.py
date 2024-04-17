import pandas as pd
import redis

# Load Excel file into DataFrame
class MigrateToDB:
    def __init__(self):
        self.df = pd.read_csv('./assignment/raw_data (4) (6).csv')
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)

    def migrate(self):
        # Sort DataFrame by device ID and time_stamp in descending order
        df_sorted = self.df.sort_values(by=['device_fk_id', 'time_stamp'], ascending=[True, False])

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
            self.r.hmset(f'device:{device_id}', data)

        print("Data transferred to Redis successfully!")

# df = pd.read_csv('./assignment/raw_data (4) (6).csv')

# # Sort DataFrame by device ID and time_stamp in descending order
# df_sorted = df.sort_values(by=['device_fk_id', 'time_stamp'], ascending=[True, False])

# # Connect to Redis
# r = redis.StrictRedis(host='localhost', port=6379, db=0)

# # Iterate over sorted DataFrame and store latest data for each device ID in Redis
# for _, row in df_sorted.iterrows():
#     device_id = row['device_fk_id']
#     data = {
#         'latitude': row['latitude'],
#         'longitude': row['longitude'],
#         'time_stamp': str(row['time_stamp']),
#         'sts': str(row['sts']),
#         'speed': row['speed']
#     }
#     # Store data in Redis hash with key as device ID
#     r.hmset(f'device:{device_id}', data)

# print("Data transferred to Redis successfully!")
