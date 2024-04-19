
# from flask_restful import Api
from src.Resource.Location import *

REDIS = 'redis'

def create_routes(api):
    try:
        api.add_resource(LatestLocation, '{}/latest-device-info/<string:device_id>'.format(REDIS))
        api.add_resource(StartEndLocation, '{}/start-end-location/<string:device_id>'.format(REDIS))
        api.add_resource(LocationPoints, '{}/location-points/<string:device_id>'.format(REDIS))
    except:
        import traceback
        print(traceback.format_exc())