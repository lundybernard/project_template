from flask import Flask

from project.lib import hello_world

app = Flask(__name__)


@app.route('/')
def hello_api():
    return hello_world()


def start_server(host='0.0.0.0', port='5000', debug=True):
    app.run(host=host, port=port, debug=debug)
