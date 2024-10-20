
from flask import Flask

app = Flask(__name__)


@app.route("/")
def Home():
    return "Flask Minimal App"
# @app.route("/user")
# def index():
#     return "Flask Minimal index App"
from controller import *

if __name__ == "__main__":
    app.run(debug=True)
