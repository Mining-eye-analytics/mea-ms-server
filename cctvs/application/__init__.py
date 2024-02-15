# application/__init__.py
from application.config import config
import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from os import path

db = SQLAlchemy()
app = Flask(__name__)



def create_app():
    environment_configuration = os.environ['CONFIGURATION_SETUP']
    app.config.from_object(environment_configuration)

    from .routes.cctvs import cctv_api_blueprint
    app.register_blueprint(cctv_api_blueprint, url_prefix='/')

    db.init_app(app)
    CORS(app)
    return app


