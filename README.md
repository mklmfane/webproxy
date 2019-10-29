# webproxy
Wuaki.tv SysAdmin/DevOps challenge

Preparing the file before uploading them 
------------------------------------------
In case you don't have root permission you can launch sudo command in front of each command. Otherwise, you can launch su -
"sudo apt install python-venv"
It is always recomended to have all files in the same parenet folder to avoid any potential confusion 
git clone https://github.com/mklmfane/webproxy.git
Ensure you go to the directory webproxy by launching the command "cd webproxy"

Ensure docker and docker compose are installed on you linux system
To install docker, you can follow instruction from the official docker docuemnetation
https://docs.docker.com/v17.09/engine/installation/linux/docker-ce/ubuntu/#install-using-the-repository

To install docker-compose, check the instructions from this link 
https://docs.docker.com/compose/install/

Then, ensure the package python3-venv is installed 
You might receive this error mentioined in the article whenever i was launching this command "python3 -m venv env".
*Error: Command '['/home/bob/Desktop/test/bin/python3.4', '-Im', 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit status 1
In this case, extract it the files from the archive downloaded from python link to find and to copy ensurepip package to /usr/lib/python3.7

This is one of the  python link. 
https://www.python.org/ftp/python/3.7.x/Python-3.7.x.tgz where x represents the last part of the python version. Depending on pyhton version you used on the system, you can choose other different python version.

In case you have issues with installing package python3-venv, you can follow the instruction from this link
https://stackoverflow.com/questions/27573710/where-is-the-ensurepip-module-source-code-pyvenv-returned-non-zero-exit-status


The following commands should work without any issues 
python3 -m venv env"
source env/bin/activate"


This is how docker-compose.yml looks like.
-----------------------------------------------------------------------------------------------------------------
version: '3.7'
services:
  flask:
    image: webapp-flask
    build: ./flask
    container_name: myflaskalt

  nginx:
    image: webapp-nginx
    build: ./nginx
    container_name: mynginxalt
    ports:
      - 8080:80
    depends_on:
      - flask
---------------------------------------------------------------------------------------------------------------------------
These are two separate folders in the folder structure  retrieved from the archive package webproxy.git. 
First folder called flask is used for web proxy and web server. The other folder nginx is used for redirecting web server traffic iniated by the web client

This is the playbook used for installing web proxy server uwsgi with flask. The proxy client gets the following response from proxy web server uwsgi that supports flask. 
---------------------------------------------------------------------------------------------------------------------------------
cat flask/Dockerfile

FROM python:3.7-buster

WORKDIR /flask

ADD . /flask
EXPOSE 8080

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "uwsgi", "--ini", "app.ini" ]
--------------------------------------------------------------------------------------------------------------------------------



Web proxy server needs a configuration file used to set up a proxy server 
-----------------------------------------------------------------------------------------
cat flask/app.ini

[uwsgi]
; This is the name of our Python file
wsgi-file = hello.py
protocol = uwsgi
module = app
; This is the name of the variable used to be called in our flask script
callable = app
master = true
; Set uWSGI to start up with 5 workers
processes = 5
; We use the port 8080 to expose our Dockerfile for the flask application
chmod-socket = 660
socket = 0.0.0.0:8080
vacuum = true
die-on-term = true


This is the flask script
-------------------------------------------------------------------------------------------------------------
cat flask/hello.py

from flask import Flask
from flask_restful import Resource, Api
from flask import Response

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}

api.add_resource(HelloWorld, '/hello')

@app.route('/hello', methods = ['GET'])
def api_hello():
    data = {"hello":"world"}

    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0:8080')
    
These are the necesssary packages to build the container with web proxy server.
---------------------------------------------------------------------------------------
cat flask/requirements.txt
Flask==1.1.1
Flask-RESTful==0.3.7
uWSGI==2.0.17.1

The second container is nginx used to send all traffic coming from web client to teh web proxy server
The configuration for teh nginx can be found under the directory nginx/nginx.conf  



This is the docker file
 cat nginx/Dockerfile
 ----------------------------------------------------------------------------
# Dockerfile-nginx
FROM nginx:latest

# Nginx will listen on this port
EXPOSE 80 443 8080

# Remove the default config file that  includes /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-available/default
RUN rm /etc/nginx/nginx.conf

# We copy the requirements file in order to install Python dependencies
COPY default /etc/nginx/sites-available/
COPY default /etc/nginx/sites-enabled/
COPY nginx.conf /etc/nginx/


EXPOSE 80 8080 443

RUN nginx -s reload
RUN sudo /etc/init.d/nginx restart



Building and executing the docker-compose playbook file  can be performed using this command 
sudo docker-compose up --build
This is the content of the docker compose template used to create two separate containers such as one for webproxy serevr and teh other for the nginx.

cat docker-compose.yml
--------------------------------------------------------------------------------------------
version: '3.7'
services:
  flask:
    image: webapp-flask
    build: ./flask
    container_name: myflaskalt

  nginx:
    image: webapp-nginx
    build: ./nginx
    container_name: mynginxalt
    ports:
      - 8080:80
    depends_on:
      - flask


Build and luanch the container in the execution to ensure they are succesfully completed after waiting for the result of  this command "sudo docker-compose up --build".

In case you have already laucnh the command and you think it is the case you modify any configuration file like nginx.conf or default in the ngix folder, you can rebuild the conatiner. The advantage of rebulding the containers is that  you won't requir to remove the containers to require downloading again the same images specified Dockerfile for the web proxy server container and for nginx .  
sudo docker-compose up -d --force-recreate

In case, you need to remove all container you can use the command "docker system prune -a"

These are the two containers built and executed
docker ps -a
------------------------------------------------------------------------------------------------------------------------------
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                  NAMES
6ffe109a68b5        webapp-nginx        "nginx -g 'daemon of…"   2 hours ago         Up 2 hours          0.0.0.0:8080->80/tcp   mynginxalt
023c4a1cf9a5        webapp-flask        "uwsgi --ini app.ini"    2 hours ago         Up 2 hours          8080/tcp               myflaskalt



This the test of the proxy client after trying to conect to proxy web server 
curl http://localhost:8080/hello
-------------------------------------------------------------------------------------
{"hello": "world"}



This is command used to get ip address of nginx container 
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mynginxalt

