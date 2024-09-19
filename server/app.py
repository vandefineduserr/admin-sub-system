from flask import Flask
from flask_cors import CORS
from waitress import serve

#modules
from me import Me
from database import DB
from project import Project
from workspace import Workspace
from authentication import Authentication


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
  

# database
db = DB()
db_clent = db.connect()


# components
auth = Authentication(app, db_clent)
me = Me(app, auth, db_clent)
workspace = Workspace(app, auth, db_clent)
project = Project(app, auth, db_clent)


if __name__ == '__main__':
    # app.run()
    serve(app, port=5001)
