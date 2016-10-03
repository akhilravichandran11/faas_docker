from flask import Flask
import docker
app = Flask(__name__)


@app.route("/")
def hello():
    cli = docker.Client(base_url='unix://var/run/docker.sock')
    contz = cli.containers()
    # count = 0
    # for keys,values in contz.items():
    #     count = count + 1
    return_string = "Hello World From Falsk "
    return  return_string

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True , port=80 )