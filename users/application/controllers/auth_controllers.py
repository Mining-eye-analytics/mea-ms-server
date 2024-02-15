import jwt
import os
from application.model.models import User
from application.helper.response import response
from werkzeug.security import generate_password_hash, check_password_hash
from application import db
import time
import requests

class Auth:
    @staticmethod
    def post_login(username, password):
        if username is None or password is None:
            return response({"errors": "Password and Username required"}, message="Login failed", code=400, status="error")

        check_hse_login = Auth.login_hse(username, password)
        # berhasil mengambil dari api hse
        if check_hse_login[0] == True:
            password_hash = generate_password_hash(password, method='scrypt')
            cek_user = User.query.filter_by(username=username).first()
            if not cek_user:
                new_user = User(username=username, password=password_hash, full_name=check_hse_login[1]["namaKaryawan"], company=check_hse_login[1]["namaPerusahaan"])
                db.session.add(new_user)
            else:
                cek_user.username = username
                cek_user.password = password_hash
                cek_user.full_name = check_hse_login[1]["namaKaryawan"]
                cek_user.company = check_hse_login[1]["namaPerusahaan"]

            db.session.commit()

            user = User.query.filter_by(username=username).first()
            
            data = user.to_json()
            data["created_at"] = str(data["created_at"])
            data["updated_at"] = str(data["updated_at"])
            payload = {
                **data, 
                "exp" : int(time.time()) + 3600*24,
                "iat" : int(time.time())
            }
            token = jwt.encode(payload, os.environ.get('SECRET_KEY'), algorithm="HS256")
            data = {**data, 'token': token}
            return response(data, message="Login From HSE success", code=200, status="success")
        
        # gagal mengambil dari api hse
        else:
            data = User.query.filter_by(username=username).first()

            if data:
                if check_password_hash(data.password, password):
                    data = data.to_json()
                    data["created_at"] = str(data["created_at"])
                    data["updated_at"] = str(data["updated_at"])
                    payload = {
                        **data, 
                        "exp" : int(time.time()) + 3600*24,
                        "iat" : int(time.time())
                    }
                    token = jwt.encode(data, os.environ.get('SECRET_KEY'), algorithm="HS256")
                    data = {**data, 'token': token}
                    return response(data, message="Login success", code=200, status="success")

                else:
                    return response(None, message="Incorrect Password", code=422, status="error")
            else:
                return response(None, message="Username Not Found", code=422, status="error")

    def login_hse(username, password):
        headers = {'x-api-key': os.environ.get("API_KEY_LOGIN")}
        data = {'username': username, 'password': password}
        try:
            response = requests.post(os.environ.get("API_URL_LOGIN"), headers=headers, json=data, timeout=5)
            if (response.status_code == 200 and response.json()['success'] == True):
                return True, response.json()
            else:
                return False, None
        except:
            print("CAN'T CONNECT INTO API HSE")
            return False, None
    
    @staticmethod
    def get_logged_in_user(request):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
            try:
                data=jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=["HS256"])
                user = User.query.filter_by(id=data['id']).first()
                if user is None:
                    meta = {
                        "message": "Invalid Authentication token!",
                        "code": 401,
                        "status": "error"
                    }
                    response = {"meta": meta, "data": None}
                    return response, 401
                
                meta = {
                    "message": "Authentication token is valid",
                    "code": 200,
                    "status": "success"
                }
                return {"meta": meta, "data": user.to_json()}, 200
            except Exception as e:
                meta = {
                    "message": f"Something went wrong, {e}",
                    "code": 401,
                    "status": "error"
                }
                response = {"meta": meta, "data": None}
                return response, 401
        else:
            meta = {
                        "message": "No Authentication token!",
                        "code": 401,
                        "status": "error"
                    }
            response = {"meta": meta, "data": None}
            return response, 401