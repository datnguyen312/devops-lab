FROM python:3.6-slim

ENV PORT=5000
EXPOSE $PORT

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

ENV GUNICORN_BIND 0.0.0.0:$PORT
CMD [ "gunicorn","service:app" ]