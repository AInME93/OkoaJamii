import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://adminuser:hardtocrackpassword@localhost/Main'
    SECRET_KEY = 'reallydifficulttoguesskey313455664'

    # # Create in-memory database
    # DATABASE_FILE = 'sample_db.sqlite'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE
    # SQLALCHEMY_ECHO = True

    # Flask-Security config
    SECURITY_URL_PREFIX = "/admin"
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = 'fhasdgihwntlgy8f'

    # Flask-Security URLs, overridden because they don't put a / at the end
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_REGISTER_URL = "/register/"

    SECURITY_POST_LOGIN_VIEW = "/admin/"
    SECURITY_POST_LOGOUT_VIEW = "/admin/"
    SECURITY_POST_REGISTER_VIEW = "/admin/"

    # Flask-Security features
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'myemail@email.com'
    MAIL_PASSWORD = 'mypassword'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True #Set to false when deploying!!!
    SQLALCHEMY_DATABASE_URI = 'postgresql://adminuser:hardtocrackpassword@localhost/Main'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI ='postgresql://adminuser:hardtocrackpassword@localhost/Test'


config = {
'development': DevelopmentConfig,
'default': DevelopmentConfig,
'testing': TestingConfig
}