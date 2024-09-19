import uuid
from flask import Response, request, jsonify, make_response, send_file
from datetime import date
from me import Me
from bson import json_util
import pandas as pd


class InvalidForm(Exception):
    "Bad form credentials"
    pass


class Project:
    def __init__(self, app, auth, db_client):
        self.app = app
        self.auth = auth
        self.workspaces = db_client["workspaces"]
        self.users = db_client["users"]

        @app.route('/api/project/<ws_name>/<projectID>/', methods=['GET', 'PUT', 'DELETE'])
        def project_detail(ws_name, projectID):
            if request.method == "GET":
                return jsonify(f"get {ws_name, projectID}"), 200

            if request.method == "PUT":
                data = request.get_json()

            if request.method == "DELETE":
                user = self.users.find_one(
                    {"email": Me.find_me(self, request).get("email")})
                workspace = self.workspaces.find_one({"name": ws_name})
                ws_user = next((item for item in workspace.get("members")
                                if item["email"] == user.get("email")), False)

                if ws_user.get("role") == 1 or ws_user.get("role") == 2:
                    try:
                        self.workspaces.update_one({"name": workspace.get('name')},
                                                   {'$pull': {"projects": projectID,
                                                              "projectsDetails": {"uid": projectID}}})
                        return jsonify("deleted"), 200
                    except TypeError:
                        return jsonify({"error": "bad request"}), 400
                else:
                    return jsonify({"error": "you do not have permission"}), 403

        @app.route('/api/project/<ws_name>/create', methods=['POST'])
        @auth.token_required()
        def project_create(ws_name):
            data = request.get_json()
            user = self.users.find_one(
                {"email": Me.find_me(self, request).get("email")})
            workspace = self.workspaces.find_one({"name": ws_name})
            ws_user = next((item for item in workspace.get(
                "members") if item["email"] == user.get("email")), False)

            if ws_user == False:
                return jsonify({"error": "you do not belong to this workspace"}), 403
            else:
                try:
                    if not data.get("name"):
                        raise InvalidForm

                    uid = str(uuid.uuid4()),
                    new_project = {
                        "uid": uid,
                        "name": data.get("name"),
                        "description": data.get("description") or "",
                        "layout": data.get("layout") or "",
                        "creationDate": str(date.today())
                    }

                    projects = workspace.get("projects")
                    projects.append(uid)

                    projects_details = workspace.get("projectsDetails")
                    projects_details.append(new_project)

                    self.workspaces.update_one({"name": workspace.get('name')},
                                               {'$set': {"projects": projects,
                                                         "projectsDetails": projects_details}})

                    return jsonify(""), 200

                except InvalidForm:
                    return jsonify({"error": "Bad credentials"}), 400

        @app.route('/api/project/<ws_name>/<projectID>/tasks/check')
        @auth.token_required()
        def check_task_status(ws_name, projectID):
            user = self.users.find_one(
                {"email": Me.find_me(self, request).get("email")})
            workspace = self.workspaces.find_one({"name": ws_name})
            ws_user = next((item for item in workspace.get(
                "members") if item["email"] == user.get("email")), False)

            if ws_user == False:
                return jsonify({"error": "You do not belong to this workspace"}), 403
            else:
                task = db_client["tasks"].find_one(
                    {"project": projectID, "status": "completed"})
                if task is not None:
                    return jsonify(json_util.dumps(task)), 200
                else:
                    return jsonify({"msg": "task not found"}), 204

        @app.route('/api/project/<ws_name>/<projectID>/search_params/', methods=['GET', 'PUT'])
        @auth.token_required()
        def project_search_params(ws_name, projectID):
            workspace = self.workspaces.find_one({"name": ws_name})
            project = next((item for item in workspace.get(
                "projectsDetails") if item["id"] == projectID), False)

            if request.method == "GET":
                if project == False:
                    return jsonify({"error": "project not found"}), 404
                


            if request.method == "POST":
                data = request.get_json()

        @app.route('/api/project/<ws_name>/<projectID>/description/', methods=['GET', 'POST'])
        @auth.token_required()
        def project_description(ws_name, projectID):
            workspace = self.workspaces.find_one({"name": ws_name})
            project = next((item for item in workspace.get(
                "projectsDetails") if item["uid"] == projectID), False)

            if request.method == "GET":
                if project == False:
                    return jsonify({"error": "project not found"}), 404
                

                print(project)
                return jsonify("description"), 200
                
                

            if request.method == "POST":
                data = request.get_json()
                print(data)
                print(project)
                
                # self.workspaces.update_one({"name": workspace.get('name')},
                #                                {'$set': {"projects": projectID,
                #                                          "projectsDetails": {"uid": projectID}}})
                    

                    

        @app.route('/api/project/<ws_name>/<projectID>/download/table', methods=['GET'])
        def download_cvs_tavle(ws_name, projectID):
            task = db_client["tasks"].find_one({"project": projectID})
            res = task.get("result")
            frame = pd.DataFrame(list(res)).to_csv('1.csv', encoding='utf-8', index=True)

            return send_file(
                '1.csv',
                mimetype='text/csv',
                download_name=f'{projectID}.csv',
                as_attachment=True
            )
