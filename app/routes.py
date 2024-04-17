
from flask_restful import Api
from src.Resource.Redis.transfer_data import TransferData, DeleteData

class create_routes:
    def __init__(self, app):
        api = Api(app)
        api.add_resource(TransferData, '/transfer_data')
        api.add_resource(DeleteData, '/delete_data')
        print("Routes created successfully!")