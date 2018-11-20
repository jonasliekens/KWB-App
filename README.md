# KWB Web Application

A little Webapp to manage the content for the KWB Grasheide Website. Written in Python 3 and Flask.

# Usage
## Configuration

Make sure to set the following environment variables with you own configuration:

```
DATABASE_URL='mysql+pymysql://user:pwd@host:port/db'
MAIL_SERVER='smtp-host'
MAIL_PORT=465
MAIL_USE_TLS=False
MAIL_USE_SSL=True
MAIL_USERNAME='username'
MAIL_PASSWORD='password'
MAIL_FROM='e-mail adress'
SECURITY_PASSWORD_SALT='pwd-salt'
SECURITY_EMAIL_SENDER='e-mail adredress'
SECURITY_KEY='security key (uuidv4)'`
```

## Start Dev Instance 

```
flask db upgrade
flask run
```

## Docker

Build the image using the command below when positioned in the KWB-App folder with a terminal
```
docker build -t {docker-hub-account}/kwb-api:1.0 .
```
Or pull from my repository
```
docker pull jonasliekens/kwb-api:1.0
```

You can set up the KWB API locally using the following docker commands

```
docker create network kwb-net
docker run --name=kwb-db --network kwb-net -e MYSQL_ROOT_PASSWORD=Str0ngPassw0rd! -p 3306:3306 -d mysql:5.6
docker run --name kwb-app --network kwb-net -e DATABASE_URL=mysql+pymysql://kwb:password@kwb-db:3306/kwb -e MAIL_SERVER=host -e MAIL_PORT=port -e MAIL_USE_TLS=False -e MAIL_USE_SSL=True -e MAIL_USERNAME=username -e MAIL_PASSWORD=password -e MAIL_FROM=email@example.com -e SECURITY_PASSWORD_SALT=salt -e SECURITY_EMAIL_SENDER=no-reply@example.com -e SECURITY_KEY=key -p 5000:5000 -d jonasliekens/kwb-api:1.0
```