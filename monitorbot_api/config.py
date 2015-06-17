import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('MB_SECRET_KEY') or 'Cannot_guess_me_hahahahaha!!! ;P'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MB_MAIL_USERNAME') or 'awillionaire@gmail.com'
    MAIL_PASSWORD = os.environ.get('MB_MAIL_PASSWORD') or 'Young1491'
    MONITOR_BOT_MAIL_SUBJECT_PREFIX = '[Monitor Bot]'
    MONITOR_BOT_MAIL_SENDER = 'Monitor Bot <awillionaire@gmail.com>'
    MONITOR_BOT_ADMIN = os.environ.get('MB_ADMIN') or 'IniUzo'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'mb-data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'mb-data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'mb-data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
