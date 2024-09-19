import re
import jwt
import uuid
import hashlib
import datetime
from datetime import timezone
from flask import request, jsonify
from functools import wraps


TOKEN_TIMEOUT_MINUTES = 1440

class Authentication:
    def __init__(self, app, db_client):
        self.app = app
        self.db_client = db_client

        @app.route('/api/login/', methods=['POST'])
        def login():
            data = request.get_json()
            pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"

            if re.match(pattern, str(data.get('email'))) is None:
                return jsonify({'message': 'Invalid credentials'}), 403
            
            if len(data.get('password')) != 64:
                return jsonify({'message': 'Invalid credentials'}), 403
            
            collection = db_client["users"]
            hashed_password = hashlib.sha256(str(data.get('password')).encode('utf-8')).hexdigest()

            user = collection.find_one({ "email": data.get('email'), "password": hashed_password })
            if user is not None:
                token = create_token(user.get("uid"), user.get("email"))
                return jsonify({'token': token}), 200

            else:
                return jsonify({'error': 'Authentication error'}), 403
            

        @app.route('/api/register/', methods=['POST'])
        def register():
            data = request.get_json()
            collection = db_client["users"]
            user = collection.find_one({"email": data.get('email')})

            if user is None:
                new_user = {"email": data.get('email'),
                            "password": hashlib.sha256(str(data.get('password')).encode('utf-8')).hexdigest(),
                            "firstname": data.get('firstname'),
                            "lastname": data.get('lastname'),
                            "uid": str(uuid.uuid4()),
                            "workspaces": []}
                
                collection.insert_one(new_user)

                token = create_token(new_user.get("uid"), new_user.get("email"))
                return jsonify({'token': token}), 200

            else:
                return jsonify({'message': 'user has already exist'}), 400

        def create_token(uid, email):
            return jwt.encode({
                "uid": uid,
                "email": email,
                "exp": datetime.datetime.now(tz=timezone.utc)
                + datetime.timedelta(minutes=TOKEN_TIMEOUT_MINUTES),
            }, key="token", algorithm="HS256")



    def token_required(self):
        def inner_decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                token = None
                key = "token"
                collection = self.db_client["users"]

                if "Authorization" in request.headers:
                    token = request.headers["Authorization"]

                if not token:
                    return jsonify({"error": "Token is missing"}), 401

                try:
                    data = jwt.decode(token, key, algorithms="HS256")
                    current_user = collection.find_one({ "uid": data.get('uid') })

                    if current_user is None:
                        return jsonify({"error": "User not found"}), 404

                except jwt.ExpiredSignatureError:
                    return jsonify({"error": "Token expired"}), 401

                except Exception as ex:
                    return jsonify({"error": "Token is invalid: " + str(ex)}), 500
                
                return f(*args, **kwargs)
                
            return decorated

        return inner_decorator
    