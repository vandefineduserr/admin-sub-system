from flask import request, jsonify
import jwt


class Me:
    def __init__(self, app, auth, db_client):
        self.app = app
        self.auth = auth
        self.collection = db_client["users"]

        @app.route('/api/me/info', methods=['GET', 'PUT'])
        @auth.token_required()
        def my_info():
            me = self.find_me(request)
            user = self.collection.find_one({"email": me.get('email')})
            if not user:
                return jsonify({"error": "user not found"}), 404

            else:
                if request.method == "GET":
                    return jsonify({"uid": user.get("uid"),
                                    "email": user.get("email"),
                                    "firstname": user.get("firstname"),
                                    "lastname": user.get("lastname"),
                                    "workspaces": user.get("workspaces")
                                    }), 200

                if request.method == "PUT":
                    data = request.get_json()
                    self.collection.update_one({"email": me.get('email')},
                                               {'$set': {"firstname": data.get("firstname"),
                                                         "lastname": data.get("lastname")}})

        
        @app.route('/api/me/change_password', methods=['PUT'])
        @auth.token_required()
        def change_my_password():
            data = request.data
            me = self.find_me(request)
            user = self.collection.find_one({"email": me.get('email')})
            if not user:
                return jsonify({"error": "user not found"}), 404

            else:
                if user.get("password") == data.get("old_password"):
                    self.collection.update_one({"email": me.get('email')},
                                               {'$set': {"password": data.get("new_password")}})
                    return jsonify({}), 200

                else:
                    return jsonify({"error": "wrong authentication credentials"}), 403

        
        @app.route('/api/me/workspaces', methods=['GET'])
        @auth.token_required()
        def my_workspaces():
            user = self.find_me(request)
            if not user:
                return jsonify({"error": "user not found"}), 404
            else:
                return jsonify({"workspaces": user.get("workspaces")}), 200

    
    def find_me(self, request):
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            key = "token"

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        return jwt.decode(token, key, algorithms="HS256")
