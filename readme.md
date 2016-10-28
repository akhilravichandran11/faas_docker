# FaaS-Function as a Service Using Docker
Use docker to demonstrate cloud applications can be setup as a set of 
microservices. Allow users to save and execute python functions on JSON object
input through a set of microservices that are deployed on demand for performing
operations like create user, create function and execute function.

The applications requires user to setup Docker swarm. Instructions to setup
Docker swarm can be found at: https://docs.docker.com/engine/swarm/
The applications has been tested on commodity servers running Ubuntu 14.x 
with Docker swarm setup using Docker 1.13.x
After the swarm is setup, the following applications/images have to be setup
on the node containing the swarm manager. Instructions below:

Tomcat/Java/Postgres Database Manager :
1. Create container for storing Postgres data
    - docker create -v /var/lib/postgresql/data --name postgres-data busybox
2. Run postgres image and attach the data container
    - docker run --name postgres -p 5432:5432 --restart=always -e POSTGRES_PASSWORD=root123#123 -d --volumes-from postgres-data postgres:9.3.6
3. Obtain Schema.sql file from /faas_docker/dbschema and run the following command(Assuming Schema.sql is in the current directory):
    - psql -U postgres -h localhost -f Schema.sql
4. Ensure /faas_docker/dbManager/dbmanager.war and /faas_docker/dbManager/DockerFile are in the same folder and run this command to build the custom tomcat image:
    - docker build -t madhat/tomcat .
5. To get Tomcat up and running, execute the following command once the above command is successful:
    - docker run --name dbmanager -d -p 8080:8080 --restart=always --link postgres:db madhat/tomcat

Db Manager is now up and running listening for requests at port 8080 and 
communicate with postgres at port 5432.
Db Manager server exposes RESTful web services for user to communicate with Db.
Public RESTful API web services can be found at /faas_docker/dbManager/Database%20Manager%20Rest%20Spec%20Brief%20Overview.info
There are brief examples for user to know how the APIs are structured and how requests can be made
User can use PostMan, DHC, ARC client extensions in Chrome and RestClient extension in Firefox
to make REST API calls to DbManager

Nginix/Python/Flask FAAS API Setup :
1. Build DockerFile provided in /faas_docker/flask_app/Dockerfile
    - docker build -t cc_flaskapp .
2. Remove Existing Container
    - docker rm -f cc_flaskapp_cont
3. Run Docker Container in required node by giving root acces to contiainer to 
talk to docker daemon , port forwading of port 80 and link container with DB Manager
    - docker run -d --name cc_flaskapp_cont -v /var/run/docker.sock:/var/run/docker.sock -p 80:80 --link dbmanager:dbmanager --restart=always --env="MODE=PROD_SWARM" cc_flaskapp

Docker CLI commands for executing microservices :
    - Microservices like Create User, Create Function , Execute Function(These commands will be executed though Docker-py(Dockers Python API) from the FAAS web app)
1. Build required image after building docker file
    - docker build -t cc_create_user_123456 .
2. Create Docker Service through swarm manager using created image and have Service's network as host
    - docker service create --name cc_create_user_123456_cont --network host cc_create_user_123456