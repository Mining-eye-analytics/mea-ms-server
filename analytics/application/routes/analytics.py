# application/user_api/routes.py
from application.controllers import analytics_controllers
from flask import Blueprint, request
from application.helper.response import response
from application.helper.get_user import User
from application.model.models import Role
import os
from application import db


analytics_api_blueprint = Blueprint('analytics_api_blueprint', __name__)

@analytics_api_blueprint.route('<idx>/video_feed', methods=['GET'])
# @User.check_access(Role.USER)
def gen_frames(idx):
    return analytics_controllers.gen_video_feed(idx)

@analytics_api_blueprint.route('list', methods=['GET'])
@User.check_access(Role.USER)
def list_analytics():
    return analytics_controllers.list_type_analytics()

@analytics_api_blueprint.route("<id>/type_analytics", methods=["POST"])
@User.check_access(Role.SUPER_ADMIN)
def type_analytics(id):
    return analytics_controllers.set_type_analytics(request, id)

@analytics_api_blueprint.route("<id>/type_analytics", methods=["GET"])
@User.check_access(Role.USER)
def type_analytics_get(id):
    return analytics_controllers.get_type_analytics(request, id)

@analytics_api_blueprint.route('assets/<path:filename>')
@User.check_access(Role.USER)
def get_assets(filename):
    return analytics_controllers.static_dir_image_cctv(filename)

@analytics_api_blueprint.route('<id>/polygon', methods=["GET", "POST"])
@User.check_access(Role.ADMIN)
def polygon_points(id):
    if request.method == "POST":
        return analytics_controllers.draw_polygon(request, id)
    return analytics_controllers.get_polygon(id)

@analytics_api_blueprint.route('<id>/distance_hd', methods=["GET", "POST"])
@User.check_access(Role.ADMIN)
def distance_hd(id):
    if request.method == "POST":
        return analytics_controllers.set_var_distance_hd(request, id)
    return analytics_controllers.get_var_distance_hd(id)

# control cctv
@analytics_api_blueprint.route('<id>/control', methods=["POST"])
@User.check_access(Role.SUPER_ADMIN)
def control(id):
    return analytics_controllers.control(request, id)