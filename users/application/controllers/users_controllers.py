from application import db
from application.model.models import User
from application.helper.response import response, objects_to_dict
from werkzeug.security import generate_password_hash, check_password_hash
import os
import jwt
import requests

# get all data
def get_users():
    try:
        users = User.query.all()
        data = objects_to_dict(users)
        
        return response(data, message="Success Get All Users", code=200, status="success")

    except Exception as e:
        print(e)

def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            return response(None, message="User Not Found", code=404, status="error")
        
        data = user.to_json()
    
        return response([data], message="Success", code=200, status="success")
    
    except Exception as e:
        print(e)
        return response(None, message="Failed to Get User", code=500, status="error")

def get_username(username):
    try:
        user = User.query.filter_by(username=username).first()
        if not user:
            return response(None, message="User Not Found", code=404, status="error")
        
        data = user.to_json()
    
        return response([data], message="True", code=200, status="success")
    
    except Exception as e:
        print(e)
        return response(None, message="Failed to Get User", code=500, status="error")

def create_user(username, password, full_name, company, role):
    try:
        new_user = User(username=username, password=generate_password_hash(password, method='scrypt'), full_name=str(full_name), company=company, role=role)
        db.session.add(new_user)
        db.session.commit()

        return response([new_user.to_json()], message="Success Add User", code=200, status="success")
    except Exception as e:
        print(e)
        return response(None, message="Failed to Add User", code=500, status="error")
    
# update data
def update_user(id,username, full_name, company, role, password):
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            return response(None, message="user Not Found", code=404, status="error")
        if username is not None: user.username = username
        if full_name is not None: user.full_name = full_name
        if company is not None: user.company = company
        if role is not None: user.role = role
        if password is not None: user.password = generate_password_hash(password, method='scrypt')

        db.session.commit()

        data = user.to_json()

        return response([data], message="Success Update user", code=200, status="success")

    except Exception as e:
        print(e)
        return response(None, message="Failed to Update User", code=500, status="error")

def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            return response(None, message="User Not Found", code=404, status="error")

        db.session.delete(user)
        db.session.commit()

        return response(None, message="Success Delete User", code=200, status="success")

    except Exception as e:
        print(e)
        return response(None, message="Failed to Delete User", code=500, status="error")