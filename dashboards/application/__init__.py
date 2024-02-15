# application/__init__.py
# import config
from application.config import config
import os
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests

from os import path

db = SQLAlchemy()
app = Flask(__name__)

list_class_cctv_webstreaming = []



def create_app():
    environment_configuration = os.environ['CONFIGURATION_SETUP']
    app.config.from_object(environment_configuration)

    from .routes.dashboards import dashboards_api_blueprint
    app.register_blueprint(dashboards_api_blueprint, url_prefix='/dashboards/')

    db.init_app(app)
    CORS(app)
    return app


