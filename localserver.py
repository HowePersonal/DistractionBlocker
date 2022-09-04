from flask import Flask
from flask_cors import CORS, cross_origin
from waitress import serve
import blockerwebsite

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route("/")
def get_blocked_sites():
    return blockerwebsite.read_file()

def start():
    serve(app, host='127.0.0.1', port=9000)
