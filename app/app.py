from flask import Flask
# from flask_restful import Api
# # from routes import TransferData, DeleteData
# from flask_cors import CORS
# from routes import create_routes
# from routes import routes
app = Flask(__name__)
# app.register_blueprint(routes)
@app.route('/')
def index():
    return 'Hello, SK !'

# create_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
