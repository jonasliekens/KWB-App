import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://kwb:kwbgrasheide1234@localhost:32769/kwb'
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Mail server settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'soulscammer'
MAIL_PASSWORD = '!SEizCV:WUw%Hl4'
MAIL_FROM = 'no-reply@brickbit.be'

SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = '5PNHiLXoM7oOQzOdTJO9F2KOj4WwEQrVeJv36aKzJnNfnDdTTl'
SECURITY_EMAIL_SENDER = 'no-reply@brickbit.be'
SECURITY_LOGIN_USER_TEMPLATE = 'login.html'

# Logging
LOG_FILE = '/tmp/kwb-app.log'

# Administrator list
ADMINS = ['jonas.liekens@brickbit.be']

# Security
WTF_CSRF_ENABLED = True
SECRET_KEY = 'a49fb3a8-795c-11e7-b5a5-be2e44b06b34'

# Pagination
POSTS_PER_PAGE=10