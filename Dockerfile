FROM debian
#FROM python:3
#FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN apt-get update
RUN apt-get install -y --no-install-recommends python3-pip python3-setuptools python3-wheel gunicorn3

WORKDIR /app

# copying requirements.txt by itself first to only have to re-run pip when necessary
COPY requirements.txt .

RUN pip3 install -r requirements.txt

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

ARG host=0.0.0.0
ARG port=8888
ARG uploads=/uploads
ARG instance=instance
ARG debug=0

VOLUME ${uploads}
VOLUME ${instance}
EXPOSE ${port}

ENV FLASK_APP "app.py"
ENV FLASK_DEBUG ${debug}
ENV port=${port}
ENV host=${host}

COPY . .

#CMD flask run -h "${host}" -p "${port}"

CMD flask db upgrade && flask run -h "${host}" -p "${port}"

# Example for deploying flask in production using gunicorn
# http://flask.pocoo.org/docs/0.12/deploying/wsgi-standalone/#gunicorn
#CMD flask db upgrade && gunicorn3 -b ${host}:${port} app:app
