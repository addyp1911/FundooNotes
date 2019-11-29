FROM python:latest
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
     && apt-get install -y default-libmysqlclient-dev  && rm -rf /var/lib/apt && mkdir /code
RUN mkdir -p /var/log/gunicorn
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

EXPOSE 8000
