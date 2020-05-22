import os
from environs import Env

# Load environment settings
env = Env()
env.read_env()

# Application settings
APP_NAME = "X Æ A-12"
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

# Flask settings
CSRF_ENABLED = True

# Flask-SQLAlchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-User settings
USER_APP_NAME = APP_NAME
USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password
USER_ENABLE_CHANGE_USERNAME = False  # Allow users to change their username
USER_ENABLE_CONFIRM_EMAIL = True  # Force users to confirm their email
USER_ENABLE_FORGOT_PASSWORD = True  # Allow users to reset their passwords
USER_ENABLE_EMAIL = True  # Register with Email
USER_ENABLE_REGISTRATION = True  # Allow new users to register
USER_REQUIRE_RETYPE_PASSWORD = True  # Prompt for `retype password` in:
USER_ENABLE_USERNAME = False  # Register and Login with username
USER_AFTER_LOGIN_ENDPOINT = 'main.home_page'
USER_AFTER_LOGOUT_ENDPOINT = 'main.home_page'

# Load environment settings
with env.prefixed("X12_"):
    SECRET_KEY = env("SECRET_KEY")
    DEBUG = env.bool("DEBUG", False)
    SQLALCHEMY_ECHO = env.bool("SQLALCHEMY_ECHO", False)
    SQLALCHEMY_DATABASE_URI = env("SQLALCHEMY_DATABASE_URI")
    MAIL_SERVER = env("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = env.int("MAIL_PORT", 587)
    MAIL_USE_SSL = env.bool("MAIL_USE_SSL", False)
    MAIL_USE_TLS = env.bool("MAIL_USE_TLS", True)
    MAIL_USERNAME = env("MAIL_USERNAME")
    MAIL_PASSWORD = env("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = env("MAIL_DEFAULT_SENDER", "X Æ A-12 Administrator")
    USER_EMAIL_SENDER_NAME = env("USER_EMAIL_SENDER_NAME")
    USER_EMAIL_SENDER_EMAIL = env("USER_EMAIL_SENDER_EMAIL")
    SERVER_PUBLIC_NOTIFICATION_KEY = env("SERVER_PUBLIC_NOTIFICATION_KEY")
    SERVER_PRIVATE_NOTIFICATION_KEY = env("SERVER_PRIVATE_NOTIFICATION_KEY")
    NOTIFICATION_SENDTO_EMAIL = env("NOTIFICATION_SENDTO_EMAIL")
    ADMINS = [
        f'"{USER_EMAIL_SENDER_NAME}" <{USER_EMAIL_SENDER_EMAIL}>',
    ]
