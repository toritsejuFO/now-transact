import os

basepath = os.path.abspath(os.path.dirname(__file__))

class Config:
    APP_NAME = os.getenv('APP_NAME', 'Now Transact')
    ENV = os.getenv('ENV', 'development')
    PORT = os.getenv('PORT', 3030)
    DEBUG = os.getenv('DEBUG')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    IP_URL = os.getenv('IP_URL')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

class DevelopmentConfig(Config):
    DEBUG = True

class TestConfig(Config):
    TESTING = True
    ENV = 'test'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' # use in memory
    # SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basepath, "test.db")}'

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'

get_env_config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'production': ProductionConfig
}
