FROM python:3.8


ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

ADD . /app
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/google_creds.json

ENTRYPOINT ["/app/docker-entrypoint.sh"]