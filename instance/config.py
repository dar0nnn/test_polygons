class Config(object):
    DEBUG = False
    CSRF_ENABLED = False
    SECRET = 'very_secret'
    SQLALCHEMY_DATABASE_URI = 'enter_db_here'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'enter_db_here'
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
