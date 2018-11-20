FROM python:3.6-alpine

WORKDIR ./kwb-api

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY migrations migrations
COPY config.py config.py

COPY run.sh run.sh
ENV FLASK_APP app/__init__.py
RUN chmod +x run.sh

EXPOSE 5000

ENTRYPOINT ["./run.sh"]