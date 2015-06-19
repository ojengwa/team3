import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('random_string') or 'Cannot_guess_me_hahahahaha!!! ;P'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MB_MAIL_USERNAME') or '<monitorbot.app@gmail.com>'
    MAIL_PASSWORD = os.environ.get('MB_MAIL_PASSWORD') or '<Monitor1>'
    MONITOR_BOT_MAIL_SUBJECT_PREFIX = '[Monitor Bot]'
    MONITOR_BOT_MAIL_SENDER = 'Monitor Bot <monitorbot.app@gmail.com>'
    MONITOR_BOT_ADMIN = os.environ.get('MB_ADMIN') or '<monitorbot.app@gmail.com>'

    BROKER_BACKEND                  = "redis" 
    BROKER_HOST                     = "localhost" 
    BROKER_PORT                     = 6379 
    BROKER_VHOST                    = "1" 
    REDIS_CONNECT_RETRY             = True 
    REDIS_HOST                      = "localhost" 
    REDIS_PORT                      = 6379 
    REDIS_DB                        = "0" 
    CELERY_SEND_EVENT               = True 
    CELERYD_LOG_LEVEL               = 'INFO' 
    CELERY_RESULT_BACKEND           = "redis" 
    CELERY_TASK_RESULT_EXPIRES      = 25 
    CELERYD_CONCURRENCY             = 8 
    CELERYD_MAX_TASKS_PER_CHILD     = 10 
    CELERY_ALWAYS_EAGER             = False


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

#BROKER_URL = 'redis://localhost:6379/0'
# redis://:Cloudbot@hostname:port/db_number
#BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}  # 1 hour.
#CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
#BROKER_TRANSPORT_OPTIONS = {'fanout_prefix': True}
#BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 43200}