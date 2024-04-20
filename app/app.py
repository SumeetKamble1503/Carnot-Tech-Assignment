import datetime
from flask import Flask, jsonify, request
import pandas as pd
import redis
from src.routes import create_routes
import json
from flask_restful import reqparse,Api
from redis.client import Redis
import os
 
def create_app():
    app = Flask(__name__)
    redis_host = os.environ.get("REDIS_DB_HOST")
    redis_port = os.environ.get("REDIS_DB_PORT")
    redis_client = Redis(host=redis_host, port=redis_port,db=0)
    app.config['REDIS_CLIENT'] = redis_client
    return app

app = create_app()
BASE_PATH = '/api/v1/'

# CORS(app)
api = Api(app, BASE_PATH)
create_routes(api)


@app.route("/health-check")
def health_check():
    response = { "status": 200 , "data": "Success" }
    return jsonify(response)    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
