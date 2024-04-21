from src.Resource.Location import *
from src.Resource.Redis import *

REDIS = 'redis'
LOCATION = 'location'

def create_routes(api):
    try:
        # Location Routes
        api.add_resource(LatestLocation, '{}/latest-device-info/<string:device_id>'.format(LOCATION))
        api.add_resource(StartEndLocation, '{}/start-end-location/<string:device_id>'.format(LOCATION))
        api.add_resource(LocationPoints, '{}/location-points/<string:device_id>'.format(LOCATION))

        # Redis Routes (Temporary: Not required)
        api.add_resource(TransferData, '{}/transfer_data_test'.format(REDIS))
        api.add_resource(DeleteData, '{}/delete'.format(REDIS))
    except:
        import traceback
        print(traceback.format_exc())