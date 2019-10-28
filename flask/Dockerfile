

FROM python:3.7-buster

WORKDIR /flask

ADD . /flask
EXPOSE 8080

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "uwsgi", "--ini", "app.ini" ]
