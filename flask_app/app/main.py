from flask import Flask
import docker
import logging
import custom_util

app = Flask(__name__)

client = docker.Client(base_url='unix://var/run/docker.sock')

@app.route("/")
def hello():
    return  "Welcome To Madhatterz - FAAS"
    

@app.route("/containers/list")    
def containers():
    containerz = client.containers()
    return  custom_util.custom_print(containerz,"<br>")
    
    
@app.route('/containers/logs/<variable>' , methods = ['GET'])
def container_logs(variable):
    log_result = ""
    try:
        log_result = client.logs(variable).replace("\n","<br>")
    except Exception as e:
        log_result =  str(e)
    return log_result
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True , port=80 )