# config.py
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    SECRET_KEY = str(os.environ.get("SECRET_KEY"))
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.environ.get("DATABASE_NAME")}.db'
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{os.environ.get("DATABASE_USER")}:{os.environ.get("DATABASE_PASSWORD")}@{os.environ.get("DATABASE_HOST")}:{os.environ.get("DATABASE_PORT")}/{os.environ.get("DATABASE_NAME")}'
    SQLALCHEMY_ECHO = False