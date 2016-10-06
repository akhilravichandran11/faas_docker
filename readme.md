# Nginix/Python/Flask FAAS API Setup
  1 - Build DockerFile provided in /faas_docker/flask_app/Dockerfile
    - docker build -t cc_flaskapp .
  2 - Run Docker Container in required node by giving root acces to contiainer to talk to docker daemon , port forwading of port 80 and link container with DB Manager
    - docker run -d --name cc_flaskapp_cont -v /var/run/docker.sock:/var/run/docker.sock -p 80:80 --link dbmanager:dbmanager --restart=always cc_flaskapp


# Docker CLI commands for executing microservices like Create User, Create Function , Execute Function(These commands will be executed though Docker-py(Dockers Python API) from the FAAS web app)
  1 - Build required image after building docker file
    - docker build -t cc_create_user_123456 .
  2 - Create Docker Service through swarm manager using created image and have Service's network as host
    - docker service create --name cc_create_user_123456_cont --network host cc_create_user_123456