# application/user_api/routes.py
from application.controllers import deviations_controllers
from flask import Blueprint, request
from application.helper.response import response
from application.helper.get_user import User
from application.model.models import Role
import os
from application import db


deviations_api_blueprint = Blueprint('deviations_api_blueprint', __name__)

@deviations_api_blueprint.route('/', methods=["GET"])
@User.token_required
@User.check_access(Role.USER)
def realtime_deviations_index():
    return deviations_controllers.index_rd()

@deviations_api_blueprint.route('<id>', methods=["GET"])
@User.token_required
@User.check_access(Role.USER)
def realtime_deviations_detail(id):
    return deviations_controllers.detail_rd(id)

@deviations_api_blueprint.route('<id>', methods=["PUT"])
@User.token_required
@User.check_access(Role.USER)
def realtime_deviations_update(id):
    return deviations_controllers.update_rd(request ,id)

@deviations_api_blueprint.route('ri', methods=["GET"])
@User.token_required
@User.check_access(Role.USER)
def realtime_images_index():
    return deviations_controllers.index_ri()

@deviations_api_blueprint.route('ri/<id>', methods=["GET"])
@User.token_required
@User.check_access(Role.USER)
def realtime_images_detail(id):
    return deviations_controllers.detail_ri(id)

@deviations_api_blueprint.route('list-type-object', methods=["GET"])
@User.token_required
@User.check_access(Role.USER)
def list_type_object():
    return deviations_controllers.type_object()

@deviations_api_blueprint.route('v1', methods=["GET"])
@User.token_required
@User.check_access(Role.USER)
def deviations():
    return deviations_controllers.get_deviations(request)

@deviations_api_blueprint.route('v2', methods=["GET"])
@User.token_required
@User.check_access(Role.USER)
def deviations_with_child():
    return deviations_controllers.get_deviations_with_child(request)

@deviations_api_blueprint.route('crossing-counting', methods=["GET"])
@User.token_required
@User.check_access(Role.USER)
def crossing_data():
    return deviations_controllers.get_crossing_counting(request)

@deviations_api_blueprint.route('crossing-counting/count-object', methods=["GET"])
@User.token_required
@User.check_access(Role.USER)
def count_crossing_data():
    return deviations_controllers.get_count_crossing_counting(request)

@deviations_api_blueprint.route('count_cctv', methods=["GET"])
@User.token_required
@User.check_access(Role.SUPER_ADMIN)
def count_cctv():
    return deviations_controllers.get_count_cctv(request)

@deviations_api_blueprint.route('count_object', methods=["GET"])
@User.token_required
@User.check_access(Role.SUPER_ADMIN)
def count_object():
    return deviations_controllers.get_count_object(request)