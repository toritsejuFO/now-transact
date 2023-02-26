import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config import get_env_config

basepath = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    connexion_app = connexion.App(os.getenv('APP_NAME'), specification_dir=basepath)
    app = connexion_app.app
    app.config.from_object(get_env_config[os.getenv('ENV', 'development')])
    db.init_app(app)
    ma.init_app(app)
    return connexion_app
