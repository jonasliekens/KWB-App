import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database
SQLALCHEMY_DATABASE_URI = 'database_url'
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Mail server settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'pwd'
MAIL_FROM = 'your_email'

SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = 'some_s3lT'
SECURITY_EMAIL_SENDER = 'your_email'
SECURITY_LOGIN_USER_TEMPLATE = 'login.html'

# Administrator list
ADMINS = ['admin_email']

# Security
WTF_CSRF_ENABLED = True
SECRET_KEY = 'sup3r_s3cr3t_k3y'

# Pagination
POSTS_PER_PAGE=10