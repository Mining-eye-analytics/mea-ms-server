from application.model.models import Role
from flask import request, jsonify
from functools import wraps
import os
import requests
import jwt

class User:
    @staticmethod
    def get_logged_in_user(request):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
            try:
                data=jwt.decode(token, os.environ.get('SECRET_KEY_USER'), algorithms=["HS256"])
                url = f"{os.environ.get('API_USER')}/{data['id']}"
                headers = {
                    "Authorization": request.headers["Authorization"]
                }
                current_user = requests.get(url, headers=headers).json()["data"]
                if current_user is None:
                    meta = {
                        "message": "Invalid Authentication token!",
                        "code": 401,
                        "status": "error"
                    }
                    response = {"meta": meta, "data": None}
                    return jsonify(response), 401
                
                meta = {
                    "message": "Authentication token is valid",
                    "code": 200,
                    "status": "success"
                }
                return {"meta": meta, "data": current_user}, 200
            except Exception as e:
                meta = {
                    "message": f"Something went wrong, {e}",
                    "code": 401,
                    "status": "error"
                }
                response = {"meta": meta, "data": str(e)}
                return jsonify(response), 401
        else:
            meta = {
                        "message": "No Authentication token!",
                        "code": 401,
                        "status": "error"
                    }
            response = {"meta": meta, "data": None}
            return response, 401
    
    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            data, status = User.get_logged_in_user(request)
            if status == 200:
                token = data.get('data')
            if not token:
                return data, status
            return f(*args, **kwargs)

        return decorated
    
    @staticmethod
    def check_access(access_level):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                token = None
                data, status = User.get_logged_in_user(request)
                if status == 200:
                    token = data.get('data')
                if not token:
                    return data, status
                role = token[0].get('role')
                if not User.role_to_access_level(role) >= access_level:
                    meta = {
                        "message": f"Role Access aborted",
                        "code": 401,
                        "status": "error"
                    }
                    return {"meta": meta, 'data': None}, 401
                return f(*args, **kwargs)
            return decorated_function
        return decorator

    def role_to_access_level(role):
        match role:
            case "user":
                return Role.USER
            case "admin":
                return Role.ADMIN
            case "super_admin":
                return Role.SUPER_ADMIN
            case default:
                return 0