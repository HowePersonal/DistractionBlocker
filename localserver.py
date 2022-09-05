from main import config, config_file
from flask import Flask
from flask_cors import CORS, cross_origin
from waitress import serve
import blockerwebsite

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route("/")
def get_blocked_sites():
    config.read(config_file)
    if config['blocker']['block'] == 'on' and config['blocker']['scheduleblock'] == 'on':
        return blockerwebsite.read_file()
    else:
        return {"sites": []}

def start():
    serve(app, host='127.0.0.1', port=9000)
