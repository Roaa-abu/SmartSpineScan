class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = "LJKKGBJDJSDDDS24534"
    UPLOAD_FOLDER = 'home/username/GP1-COPY/app/static/img/uploads'

    SESSION_COOKIE_SECURE =True
    ENV="Production"

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = False
    UPLOAD_FOLDER= './app/static/img/uploads'
    SESSION_COOKIE_SECURE =False
    ENV="Development"

class TestingConfig(Config):
    TESTING = True
    UPLOAD_FOLDER= './app/static/img/uploads'
    SESSION_COOKIE_SECURE =False
    ENV = "testing"

