# FaaS-Function as a Service Using Docker
Functions as a Service Implementation Using Docker and Docker Swarm


For better view, please use the raw view to check contents

URL for demo video: https://www.youtube.com/watch?v=prH4kQjR5gE


Use docker to demonstrate cloud applications can be setup as a set of
microservices. Allow users to save and execute python functions on JSON object
input through a set of microservices that are deployed on demand for performing
operations like create user, create function and execute function.

The applications requires user to setup Docker swarm. Instructions to setup
Docker swarm can be found at: https://docs.docker.com/engine/swarm/
The applications has been tested on commodity servers running Ubuntu 14.x
with Docker swarm setup using Docker 1.13.x
After the swarm is setup, the following applications/images have to be setup
on the node containing the swarm manager.

The current setup on ThoTh lab has a manager node on VM1 and node 1(VM2), node 2(VM3),
node 3(VM4) are setup as workers. Microservices are deployed on available nodes
using bin packing algorithm. Services deployed on the swarm run until explicitly removed
and can be deployed either in global/replicated mode.

The application contains components that are deployed to handle user requests
and manage microservice deployment on docker swarm. The instructions to deploy
them are captured below:

Tomcat/Java/Postgres Database Manager - Provides internal RESTful APIs to manage postgres database :
1. Create container for storing Postgres data
    - docker create -v /var/lib/postgresql/data --name postgres-data busybox
2. Run postgres image and attach the data container to bring up the postgres database
    - docker run --name postgres -p 5432:5432 --restart=always -e POSTGRES_PASSWORD=root123#123 -d --volumes-from postgres-data postgres:9.3.6
3. Obtain Schema.sql file from /faas_docker/dbschema and run the following command(Assuming Schema.sql is in the current directory):
    - psql -U postgres -h localhost -f Schema.sql
4. Ensure /faas_docker/dbManager/dbmanager.war and /faas_docker/dbManager/DockerFile are in the same folder and run this command to build the custom tomcat image for dbManager:
    This can be run on /faas_docker/dbManager folder
    - docker build -t madhat/tomcat .
5. To get Tomcat up and running, execute the following command once the above command is successful:
    - docker run --name dbmanager -d -p 8080:8080 --restart=always --link postgres:db madhat/tomcat

Db Manager is now up and running listening for requests.
Db Manager server exposes RESTful web services for API Gateway to communicate with Db.
RESTful API web services can be found at /faas_docker/dbManager/Database%20Manager%20Rest%20Spec%20Brief%20Overview.info
There are brief examples for user to know how the APIs are structured and how requests can be made
User can use PostMan, DHC, ARC client extensions in Chrome and RestClient extension in Firefox
to make REST API calls to DbManager

Nginix/Python/Flask FAAS API Gateway Setup - For user to provision requests on demand on the cloud application:
1. Build DockerFile provided in /faas_docker/flask_app/Dockerfile
    - docker build -t cc_flaskapp .
2. Remove Existing Container(Ignore if first time install)
    - docker rm -f cc_flaskapp_cont
3. Run Docker Container on the manager node based on the mode(swarm mode is used in ThoThLaab) you want it to be up in:
    - For Swarm Service Mode
        docker run -d --name cc_flaskapp_cont -v /var/run/docker.sock:/var/run/docker.sock -p 80:80 --link dbmanager:dbmanager --restart=always --env="MODE=PROD_SWARM" cc_flaskapp
    - For Swarm Container Mode
        docker run -d --name cc_flaskapp_cont -v /var/run/docker.sock:/var/run/docker.sock -p 80:80 --link dbmanager:dbmanager --restart=always --env="MODE=PROD" cc_flaskapp
    - For Local Mode
        docker run -d --name cc_flaskapp_cont -v /var/run/docker.sock:/var/run/docker.sock -p 80:80 --link dbmanager:dbmanager --restart=always cc_flaskapp

Flask App is now up and listening to requests on port 80 of the manager.
RESTful API web service details can be found at - /faas_docker/flask_app/Faas_api_format.md
User can refer to the public API doc to identify operations they want to perform.
Function Declaration and JSON input and output data format can be found at - /faas_docker/flask_app/Function_format.md


Private Image Registry - To host microservice images which are deployed for user request:
This registry is already setup on the manager node on ThoThLab with the images already uploaded.
The following command can be executed to setup a private registry of our own:
 docker run -d -p 5000:5000 --restart=always --name registry registry:2
 This sets up the registry container and it can be accessed through port 5000

To deploy microservice images to the registry, the following commands need to be executed on
/faas_docker/func_microservices/function-create,update,delete,execute folder and
/faas_docker/func_microservices/user-create,update,delete folder
A reference for these commands be found at /faas_docker/func_microservices/docker_build_commands.txt
1. docker build -t <image-name> .
2. docker tag <image-name> <registry-ip-address>:5000/<image-name>
3. docker push <registry-ip-address>:5000/<image-name>

The docker registry needs to be setup with names indicated in the docker_build_commands.txt for it to
function correctly

Monitoring Service - To monitor resource utlization:
This uses cAdvisor collector, elasticSearch to maintain and search data, Kibana to display indexed data in elasticSearch.
This service is already setup on ThoThLab to monitor memory,cpu,network utilzation
Refer to /faas_docker/Commands%20for%20monitoring%20service for commands to setup this service and change IP address to reflect
the nodes where elasticSearch is actually deployed

The following is a summary of all the files that are present in the repository:
Filename                                Purpose                     New/Modified/Old                   Comments
JSON Settings for Kibana    Used to setup dashboard visualization         New              Can be ignored if user is creating custom Kibana visualizations
DockerServiceCommands    Steps for running service thru docker py         New               Developer instructions
Commands for monitoring service     Setup monitoring service in swarm     New               Ignore if monitoring is not necessary

screenshots/*    Contains images captured for operation in subfolders     New/Modified      File name provides description of the operation performed

misc/py_apps/Python_client.py   Python client to interact with API Gateway  New             Menu driven for user to perform single,bulk operations on application
misc/create_user/*      Folder containing intial test bits for create user  Old             Can be used to create image for intial test bits written
misc/function.py    File containing sample function that can be executed    New             Adds numbers in a list in python
misc/create_user.py,
misc/create_function.py, Initial test bit files to perform microservices    Old             Can be ignored. Gives insight into intial attempts made
misc/execute/*      Test bits used to get execute function up and running   New             Can be ignored. Gives insight into approaches available to execute code thru python modules
misc/docker_py_commands.py  Commands to use docker py for deploying container   New/Modified    Can be ignored. Stepping stone for docker py
misc/docker commands.txt    Commands to build and link containers           Old             Can be ignored. Docker internal investigation
misc/Dockerfile         Sample docker file to deploy python application     Old             Starting point to deploy images with code
misc/tst.py             Sample python file                                  Old             Ignore

func_microservices/docker-compose.yml  Sample yaml file to deploy applocation  Old         Ignore unless docker compose is used
func_microservices/docker_build_commands.txt  Commands to setup microservice images  New/Modified   Required only if user is setting up the images on a private registry of their choice
func_microservices/user/create/app.py           Main app to create user     New/Modified    Contains core logic to interact with dbmanager
func_microservices/user/create/app_correct.py  Test app to check create user on container New/Modified      Test file to check run on container   
func_microservices/user/create/app_swarm_check.py Test app to check create user on swarm    New/Modified    Test file to check run on swarm
func_microservices/user/create/util.py      Helper class for user create operation  New/Modified            Helper to manage API urls, manage environment variables passed
func_microservices/user/create/Dockerfile   Image file to create microservice image New/Modified            Used to create images that can be deployed on private registry

func_microservices/user/delete/app.py       Main app to delete user     New/Modified    Contains core logic to interact with dbmanager
func_microservices/user/delete/util.py      Helper class for user delete operation  New/Modified            Helper to manage API urls, manage environment variables passed
func_microservices/user/delete/Dockerfile   Image file to create microservice image New/Modified            Used to create images that can be deployed on private registry

func_microservices/user/update/app.py   Main app to update user     New/Modified    Contains core logic to interact with dbmanager
func_microservices/user/update/util.py   Helper class for user update operation  New/Modified            Helper to manage API urls, manage environment variables passed
func_microservices/user/update/Dockerfile   Image file to create microservice image New/Modified            Used to create images that can be deployed on private registry

func_microservices/function/create/app.py   Main app to create function New/Modified    Contains core logic to interact with dbmanager
func_microservices/function/create/util.py      Helper class for function create operation  New/Modified            Helper to manage API urls, manage environment variables passed
func_microservices/function/create/func_compile Helper class to manage compile checks on function New/Modified  Used to check syntax errors for user defined function
func_microservices/function/create/Dockerfile   Image file to create microservice image New/Modified            Used to create images that can be deployed on private registry

func_microservices/function/delete/app.py   Main app to delete function New/Modified    Contains core logic to interact with dbmanager    
func_microservices/function/delete/util.py  Helper class for function delete operation  New/Modified            Helper to manage API urls, manage environment variables passed
func_microservices/function/delete/Dockerfile Image file to create microservice image New/Modified            Used to create images that can be deployed on private registry

func_microservices/function/execute/app.py  Main app to execute function New/Modified    Contains core logic to execute user code, interact with dbmanager
func_microservices/function/execute/util.py Helper class for function execute operation  New/Modified            Helper to manage API urls, manage environment variables passed
func_microservices/function/execute/func_exec.py Helper class to manage user function execution environment  New/Modified   Used for setting up environment for executing code
func_microservices/function/execute/Dockerfile Image file to create microservice image New/Modified            Used to create images that can be deployed on private registry

func_microservices/function/update/app.py   Main app to update function New/Modified    Contains core logic to interact with dbmanager
func_microservices/function/update/util.py      Helper class for function update operation  New/Modified            Helper to manage API urls, manage environment variables passed
func_microservices/function/update/func_compile Helper class to manage compile checks on function New/Modified  Used to check syntax errors for user defined function
func_microservices/function/update/Dockerfile   Image file to create microservice image New/Modified            Used to create images that can be deployed on private registry

flask_app/requirements.txt      Requirements to build flask app image       Old         Needed for succesful flask app build
flask_app/nginx.conf            Configuration for the nginx server          Old         Needed for server configuration
flask_app/docker_build_commands.txt Commands to build and deploy flask app  Old
flask_app/Dockerfile            Image file to build the flask app           Old         Used to create flask app to be deployed on docker manager
flask_app/app/constants.py      Constants for the application               Old         Image names, swarm service names, status codes for operations
flask_app/app/custom_util.py    Util for managing environment setup for service deployment  Old     Operations to manage data
flask_app/app/db_manager_handler.py Handles requests/response to dbmanager      Old         REST API client to make internal calls to dbManager
flask_app/app/docker_util.py     Make docker py calls to deploy/remove service      New/Modified        Contains util to generate unique service names
flask_app/app/func_exec.py       Sample user function execute logic         New/Modified        Ignore. Initial attempt to try execute function code
flask_app/app/main.py            Main application to handle API gateway request         Old/Modified        REST API request/response that user interacts with to perform operations
flask_app/app/uwsgi.ini          Additional configuration for nginx         Old
flask_app/Faas_api_format.md     Added readme for Faas api request format   New
flask_app/Function_format.md     Added readme for function format           New
dbschema/Schema.sql         Schema file to setup the database and tables    Old         Refer to instructions in README to deploy

dbManager/dbmanager.war     Archive file containing package code for Tomcat     Old/Modified    Gets deployed on tomcat to setup dbManager
dbManager/dbService-README  Details to deploy dbmanager service                 Old
dbManager/Dockerfile        Image file to create dbmanager image                Old         Creates image for dbmanager deployment
dbManager/Database Manager Rest Spec Brief Overview.info    REST API web service specification for dbmanager        Old     For internal reference only. Not public APIs
dbManager/Code/dbmanager/pom.xml    Maven build file to create war file         Old         Create dbmanager.war file to be deployed on Tomcat
dbManager/Code/dbmanager/.project          Project file for Eclipse                        Old
dbManager/Code/dbmanager/.classpath        Classpath for Eclipse           Old
dbManager/Code/dbmanager/target/*          Contains temporary files to create war file using Maven Old/Modified    Contains external jars downloaded for project requirement
dbManager/Code/dbmanager/.settings/*       Configuration files for eclipse code        Old
dbManager/Code/dbmanager/src/main/main.iml Eclipse default project build file      Old
dbManager/Code/dbmanager/src/main/webapp/index.jsp Default file for web application        Old
dbManager/Code/dbmanager/src/main/webapp/WEB-INF/web.xml   Define servlets for dbmanager       Old     Required for Java webapp to manipulate requests
dbManager/Code/dbManager/Code/dbmanager/src/main/resources/hibernate.cfg.xml    Contains postgres connection data and annotated classe details  Old     Gives driver/connection info for database connection
dbManager/Code/dbmanager/src/main/java/com/cc/faas/dbmanager/rest/UserHandler.java      Contains APIs for user resource manipulation    Old     REST APIs for request/response using JSON for user
dbManager/Code/dbmanager/src/main/java/com/cc/faas/dbmanager/rest/RequestHandler.java      Contains APIs for request resource manipulation    Old     REST APIs for request/response using JSON for request
dbManager/Code/dbmanager/src/main/java/com/cc/faas/dbmanager/rest/FunctionHandler.java      Contains APIs for function resource manipulation    Old     REST APIs for request/response using JSON for function
dbManager/Code/dbmanager/src/main/java/com/cc/faas/dbmanager/rest/util/Helper.java      Utility to generate JSON string for generating error response  Old
dbManager/Code/dbmanager/src/main/java/com/cc/faas/dbmanager/rest/util/Message.java     Error message object returned to the user Bad Request/Internal Server Error     Old
dbManager/Code/dbmanager/src/main/java/com/cc/faas/dbmanager/rest/service/UserServiceImpl.java      Service module to manage user CRUD operations   Old
dbManager/Code/dbmanager/src/main/java/com/cc/faas/dbmanager/rest/service/RequestServiceImpl.java   Service module to manage request CRUD operations   Old
dbManager/Code/dbmanager/src/main/java/com/cc/faas/dbmanager/rest/service/FunctionServiceImpl.java  Service module to manage function CRUD operations   Old
dbManager/Code/dbmanager/src/main/java/com/cc/faas/dbmanager/rest/pojo/User.java    JSON object for user CRUD API request/response  Old
dbManager/Code/dbmanager/src/main/java/com/cc/faas/dbmanager/rest/pojo/Request.java JSON object for request CRUD API request/response  Old
dbManager/Code/dbmanager/src/main/java/com/cc/faas/dbmanager/rest/pojo/Function.java JSON object for function CRUD API request/response  Old
dbManager/Code/dbmanager/src/main/java/com/cc/faas/dbmanager/rest/entity/UserEntity.java    JAVAX persistence POJO for representing User table in database  Old
dbManager/Code/dbmanager/src/main/java/com/cc/faas/dbmanager/rest/entity/RequestEntity.java JAVAX persistence POJO for representing Request table in database  Old
dbManager/Code/dbmanager/src/main/java/com/cc/faas/dbmanager/rest/entity/FunctionEntity.java    JAVAX persistence POJO for representing Function table in database  Old
dbManager/Code/dbmanager/src/main/java/com/cc/faas/dbmanager/rest/dao/UserDaoImpl.java  DAO object to manipulate User table through Hibernate calls Old
dbManager/Code/dbmanager/src/main/java/com/cc/faas/dbmanager/rest/dao/RequestDaoImpl.java   DAO object to manipulate Request table through Hibernate calls Old
dbManager/Code/dbmanager/src/main/java/com/cc/faas/dbmanager/rest/dao/FunctionDaoImpl.java  DAO object to manipulate Function table through Hibernate calls Old
dbManager/Code/dbmanager/src/main/java/com/cc/faas/dbmanager/rest/dao/HibernateUtil.java    Session manager object to manage connections to the database through Hibernate  Old
dbManager/Code/dbmanager/src/main/java/com/cc/faas/dbmanager/rest/constants/ExceptionConstants.java  Constants to create error message strings for Bad request/Internal Server error    Old
