# application/user_api/routes.py
from application.controllers import cctvs_controllers
from flask import Blueprint, request
from application.helper.get_user import User
from application.model.models import Role
from application.helper.response import response
import os


cctv_api_blueprint = Blueprint('cctv_api_blueprint', __name__)

# CREATE
@cctv_api_blueprint.route('/create', methods=['POST'])
@User.token_required
@User.check_access(Role.SUPER_ADMIN)
def create_cctv():
    link_rtsp = request.form.get('link_rtsp')
    name = request.form.get('name')
    location = request.form.get('location')
    ip = request.form.get('ip')
    username = request.form.get('username')
    password = request.form.get('password')
    type_analytics = request.form.get('type_analytics')

    return cctvs_controllers.create_cctv(link_rtsp, name, location, ip, username, password, type_analytics)

# READ
@cctv_api_blueprint.route('/', methods=['GET'])
@User.token_required
@User.check_access(Role.USER)
def get_cctvs():
    return cctvs_controllers.get_cctvs()

# READ
@cctv_api_blueprint.route('/server', methods=['GET'])
def get_cctvs_from_server():
    api_key = request.headers.get('API-Key')
    if api_key == os.environ.get('SECRET_KEY'):
        return cctvs_controllers.get_cctvs()
    else:
        return response(None, message="Failed to Get CCTV", code=400, status="error")

@cctv_api_blueprint.route('/<id>', methods=['GET'])
@User.token_required
@User.check_access(Role.USER)
def get_cctv(id):
    return cctvs_controllers.get_cctv(id)

@cctv_api_blueprint.route('/server/<id>', methods=['GET'])
def get_cctv_from_server(id):
    api_key = request.headers.get('API-Key')
    if api_key == os.environ.get('SECRET_KEY'):
        return cctvs_controllers.get_cctv(id)
    else:
        return response(None, message="Failed to Get CCTV", code=400, status="error")

# UPDATE
@cctv_api_blueprint.route('/<id>', methods=['PUT'])
@User.token_required
@User.check_access(Role.SUPER_ADMIN)
def update_cctv(id):
    link_rtsp = request.form.get('link_rtsp')
    name = request.form.get('name')
    location = request.form.get('location')
    ip = request.form.get('ip')
    username = request.form.get('username')
    password = request.form.get('password')
    type_analytics = request.form.get('type_analytics')

    return cctvs_controllers.update_cctv(id, link_rtsp, name, location, ip, username, password, type_analytics)

# DELETE
@cctv_api_blueprint.route('/<id>', methods=['DELETE'])
@User.token_required
@User.check_access(Role.SUPER_ADMIN)
def delete_cctv(id):
    return cctvs_controllers.delete_cctv(request, id)