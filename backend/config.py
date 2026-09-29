import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        BASE_DIR,
        'database',
        'placement_portal.db'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "placementportaljwtsecret"
    )
    
    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False

    MAIL_USERNAME = None
    MAIL_PASSWORD = None

    MAIL_DEFAULT_SENDER = "placementportal@example.com"