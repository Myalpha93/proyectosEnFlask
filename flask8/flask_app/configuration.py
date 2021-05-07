class BaseConfig(object):
    'Base configuracion'
    SECRET_KEY = 'Key'
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:12345678@localhost:5433/pyalmacen"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class ProductionConfig(BaseConfig):
    'Produccion configuracion'
    DEBUG = False
class DevelopmentConfig(BaseConfig):
    'Desarrollo configuracion'
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'Desarrollo key'
    