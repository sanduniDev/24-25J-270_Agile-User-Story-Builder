# app.py
from flask import Flask
from flask_socketio import SocketIO
from api.routes import create_blueprint

socketio = None
def create_app():
    app = Flask(__name__)
    api_blueprints = create_blueprint()
    app.register_blueprint(api_blueprints, url_prefix="/api")
    
    return app
