from flask import Flask
from flask_cors import CORS
from waitress import serve

from ai_hr import AiRequests

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

ai = AiRequests(app)


if __name__ == "__main__":
    serve(app, port=9000)
