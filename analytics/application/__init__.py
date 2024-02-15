# application/__init__.py
# import config
from application.config import config
import os
from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import requests

from os import path
from application.helper import stream_cctv, analytics

db = SQLAlchemy()
app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")

def create_app():
    environment_configuration = os.environ['CONFIGURATION_SETUP']
    app.config.from_object(environment_configuration)

    from .routes.analytics import analytics_api_blueprint
    app.register_blueprint(analytics_api_blueprint, url_prefix='/')

    # generate_stream_cctvs()
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    CORS(app)
    return app, socketio


