import os
from distutils.util import strtobool

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Mail server settings
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = os.environ.get('MAIL_PORT')
MAIL_USE_TLS = strtobool(os.environ.get('MAIL_USE_TLS'))
MAIL_USE_SSL = strtobool(os.environ.get('MAIL_USE_SSL'))
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_FROM = os.environ.get('MAIL_FROM')

SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
SECURITY_EMAIL_SENDER = os.environ.get('SECURITY_EMAIL_SENDER')
SECURITY_LOGIN_USER_TEMPLATE = 'login.html'

# Logging
LOG_FILE = '/tmp/kwb-app.log'

# Administrator list
ADMINS = ['jonas.liekens@brickbit.be']

# Security
WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get('SECURITY_KEY')

# Pagination
POSTS_PER_PAGE=10