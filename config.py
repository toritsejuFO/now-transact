import os

basepath = os.path.abspath(os.path.dirname(__file__))

class Config:
    APP_NAME = os.getenv('APP_NAME')
    ENV = os.getenv('ENV')
    PORT = os.getenv('PORT')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

class DevelopmentConfig(Config):
    FLASK_DEBUG = True

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'sqlite3://{os.path.join(basepath, "test.db")}'

class ProductionConfig(Config):
    FLASK_DEBUG = False

get_env_config = {
    'development': DevelopmentConfig
}
