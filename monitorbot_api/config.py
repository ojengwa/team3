import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('MB_SECRET_KEY') or 'Cannot_guess_me_hahahahaha!!! ;P'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.mailgun.org'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MB_MAIL_USERNAME') or 'postmaster@sandboxcb453b06494e49b5bcdcabd6cb10d04d.mailgun.org'
    MAIL_PASSWORD = os.environ.get('MB_MAIL_PASSWORD') or '3c00d838197e17d1b3d7737ccd0269fd'
    MONITOR_BOT_REPORT_SUBJECT = 'Monitor Bot Check Report'
    MONITOR_BOT_MAIL_SENDER = 'Monitor Bot <monitorbot.app@gmail.com>'
    MONITOR_BOT_ADMIN = os.environ.get('MB_ADMIN') or 'Ini Uzo'

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
