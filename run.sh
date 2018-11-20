#!/bin/sh
flask db migrate
flask translate compile
exec gunicorn -b :5000 --access-logfile - --error-logfile - app:app