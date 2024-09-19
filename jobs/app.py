import threading
import uuid
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from waitress import serve
from constants import HOST
from composer import Parser
from pymongo import MongoClient

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# components
parser = Parser()

def check_auth(token):
    if "Authorization" in request.headers:
        r = requests.get(url=f'{HOST}/api/connect', headers={'Authorization': token})
        data= r.json()
        if data.get("connected") == True:
            return True
        else:
            return False
    else:
        return False

@app.route('/parse/ping', methods=['GET'])
def ping():
    if "Authorization" in request.headers:
        token = request.headers["Authorization"]
        is_available = check_auth(token)
        if is_available == True:
            return jsonify({"echo": "Parsers are avilable"}), 200


@app.route('/parse/find', methods=['POST'])
def find_cv():

    # if "Authorization" in request.headers:
    #     token = request.headers["Authorization"]
    #     is_available = check_auth(token)
    #     if is_available == True:
    #         print(request.data)
    #         return jsonify({"echo": "Parsers are avilable"}), 200
    #     else:
    #         return jsonify({"error": "Not Authorised"}), 401


    data = request.get_json()

    mongo_client = MongoClient("mongodb://user:Q3AM3UQ867SPQQA43P2F@mongodb:27017/?retryWrites=true&w=majority")["ws-admin-system"]
    ws = mongo_client["workspaces"].find_one({"name": data["ws_name"]})
    ws_tasks = ws.get("tasks")

    task = {
        "id": str(uuid.uuid4()),
        "status": "started",
        "project": data.get("project"),
        "result": []
    }

    download_thread = threading.Thread(target=parser.parse, name="Downloader", args=(data["search_params"], mongo_client, task["id"],))
    download_thread.start()

    ws_tasks.append(task["id"])

    mongo_client["tasks"].insert_one(task)
    mongo_client["workspaces"].update_one({"name": data["ws_name"]}, 
                                          {'$set': {"tasks": ws_tasks}})

    return jsonify({"message": "Job started"}), 200



if __name__ == '__main__':
    # app.run()
    serve(app, port=5173)