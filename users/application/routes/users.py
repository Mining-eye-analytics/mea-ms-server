# application/routes/users.py
from application.controllers import users_controllers
from flask import request, Blueprint
from application.helper.decorator import token_required, check_access
from application.helper.response import response
from application.model.models import Role
from application.controllers.auth_controllers import Auth
import os

user_api_blueprint = Blueprint('user_api_blueprint', __name__)

# CREATE / POST
@user_api_blueprint.route('/create', methods=['POST'])
@token_required
@check_access(Role.SUPER_ADMIN)
def post_register():
    company = request.form.get('company')
    full_name = request.form.get('full_name')
    username = request.form.get('username')
    role = request.form.get('role')
    password = request.form.get('password')

    return users_controllers.create_user(username, password, full_name, company, role)

@user_api_blueprint.route('/', methods=['POST'])
def post_register_from_server():
    company = request.form.get('company')
    full_name = request.form.get('full_name')
    username = request.form.get('username')
    role = request.form.get('role')
    password = request.form.get('password')
    api_key = request.headers.get('API-Key')
    if api_key == os.environ.get('SECRET_KEY'):
        return users_controllers.create_user(username, password, full_name, company, role)
    else:
        return response(None, message="Failed to register user", code=400, status="error")

# READ / GET
@user_api_blueprint.route('/', methods=['GET'])
@token_required
@check_access(Role.USER)
def get_users():
    return users_controllers.get_users()

@user_api_blueprint.route('/<id>', methods=['GET'])
@token_required
@check_access(Role.USER)
def get_user(id):
    return users_controllers.get_user(id)

# UPDATE
@user_api_blueprint.route('/<id>', methods=['PUT', 'DELETE'])
@token_required
@check_access(Role.SUPER_ADMIN)
def action_user(id):
    if request.method == 'PUT':
        company = request.form.get('company')
        full_name = request.form.get('full_name')
        username = request.form.get('username')
        role = request.form.get('role')
        password = request.form.get('password')
        return users_controllers.update_user(id, username, full_name, company, role, password)
    elif request.method == 'DELETE':
        return users_controllers.delete_user(id)


@user_api_blueprint.route('/<username>/exists', methods=['GET'])
@token_required
@check_access(Role.USER)
def get_username(username):
    return users_controllers.get_username(username)


@user_api_blueprint.route('/login', methods=['POST'])
def post_login():
    username = request.form.get('username')
    password = request.form.get('password')
    return Auth.post_login(username, password)

