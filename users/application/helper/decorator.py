from application.model.models import Role
from flask import request, abort
from functools import wraps
from application.controllers.auth_controllers import Auth

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        data, status = Auth.get_logged_in_user(request)
        if status == 200:
            token = data.get('data')
        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated

def check_access(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            data, status = Auth.get_logged_in_user(request)
            if status == 200:
                token = data.get('data')
            if not token:
                return data, status
            role = token.get('role')
            if not role_to_access_level(role) >= access_level:
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