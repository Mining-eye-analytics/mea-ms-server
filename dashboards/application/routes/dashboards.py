# application/user_api/routes.py
from application.controllers import dashboards_controllers
from flask import Blueprint, request
from application.helper.response import response
from application.helper.get_user import User
from application.model.models import Role
import os
from application import db


dashboards_api_blueprint = Blueprint('dashboards_api_blueprint', __name__)

@dashboards_api_blueprint.route('notification_profile', methods=["GET"])
@User.token_required
@User.check_access(Role.USER)
def notification_profile():
    return dashboards_controllers.get_notification_profile(request)

@dashboards_api_blueprint.route('validation_profile', methods=["GET"])
@User.token_required
@User.check_access(Role.USER)
def validation_profile():
    return dashboards_controllers.get_validation_profile(request)

@dashboards_api_blueprint.route('validator_profile', methods=["GET"])
@User.token_required
@User.check_access(Role.USER)
def validator_profile():
    return dashboards_controllers.get_validator_profile(request)

@dashboards_api_blueprint.route('total_average_validation', methods=["GET"])
@User.token_required
@User.check_access(Role.USER)
def total_average_validation():
    return dashboards_controllers.get_total_average_validation(request)

@dashboards_api_blueprint.route('validation_distribution', methods=["GET"])
@User.token_required
@User.check_access(Role.USER)
def validation_distribution():
    return dashboards_controllers.get_validation_distribution(request)