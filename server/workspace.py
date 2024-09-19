import uuid
import json

from me import Me
from bson import json_util
from flask import request, jsonify


class InvalidForm(Exception):
    "Bad form credentials"
    pass

class Workspace:
    def __init__(self, app, auth, db_client):
        self.app = app
        self.auth = auth
        self.workspaces = db_client["workspaces"]
        self.users = db_client["users"]


        @app.route('/api/connect', methods=['GET'])
        @auth.token_required()
        def connect():
            return jsonify({"connected": True})


        @app.route('/api/workspace/<ws_name>', methods=['GET', 'PUT', 'DELETE'])
        @auth.token_required()
        def workspace_managment(ws_name):
            def parse_json(data):
                return json.loads(json_util.dumps(data))
            
            user = self.users.find_one({"email": Me.find_me(self, request).get("email") })
            workspace = self.workspaces.find_one({"name": ws_name})

            if workspace is not None:
                ws_user = next((item for item in workspace.get("members") if item["email"] == user.get("email")), False)
                
                if ws_user == False:
                    return jsonify({"error": "you do not belong to this workspace"}), 403
                
                else:
                    if request.method == "GET":
                        return jsonify(parse_json(workspace)), 200
                    
                    #owner only
                    if request.method == "DELETE":
                        if ws_user.get("role") == 2:
                            self.workspaces.delete_one({"name": ws_name})
                            return jsonify(workspace.get("name")), 200
                        else:
                            return jsonify({"error": "you do not have permission for this operation"}), 403
                    
                    #admin or owner
                    if request.method == "PUT":
                        if ws_user.get("role") == 1 or ws_user.get("role") == 2:
                            return jsonify(workspace.get("name")), 200
                        else:
                            return jsonify({"error": "you do not have permission for this operation"}), 403
            
            else:
                return jsonify({"error": "workspace does not exist"}), 404
       

        @app.route('/api/workspace/create', methods=['POST'])
        @auth.token_required()
        def workspace_create():
            data = request.get_json()
            user = self.users.find_one({"email": Me.find_me(self, request).get("email") })

            if (user is not None or data.get("name") is not None):
                try:
                    if self.workspaces.find_one({"name": data.get("name")}) is not None:
                        raise InvalidForm
                    
                    member = {
                        "uid": user.get("uid"),
                        "firstname": user.get("firstname"),
                        "lastname": user.get("lastname"),
                        "email": user.get("email"),
                        "role": 2
                    }

                    uid = str(uuid.uuid4()),
                    members = [member]
                    user["workspaces"].append(data.get("name"))

                    new_workspace = {
                        "uid": uid,
                        "name": data.get("name"),
                        "type": int(data.get("type")),
                        "members": members,
                        "invitations": data.get("invitations"),
                        "projects": data.get("projects"),
                        "projectsDetails": data.get("projectsDetails"),
                        "tasks": data.get("tasks")
                    }

                    self.workspaces.insert_one(new_workspace)
                    self.users.update_one({"email": user.get('email')},
                                          {'$set': {"workspaces": user.get("workspaces")}})
                    return jsonify({'ws_name': data.get("name")}), 200

                except InvalidForm:
                    return jsonify({"error": "Workspace has already exist"}), 400
                
            return jsonify("error: invalid request"), 400