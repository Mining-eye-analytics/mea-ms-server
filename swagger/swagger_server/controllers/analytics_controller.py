import connexion
import six

from swagger_server.models.set_distance_hd_request import SetDistanceHDRequest  # noqa: E501
from swagger_server.models.set_polygon_points_request import SetPolygonPointsRequest  # noqa: E501
from swagger_server.models.set_type_analytics_request import SetTypeAnalyticsRequest  # noqa: E501
from swagger_server import util


def generate_frame(id):  # noqa: E501
    """Generate Frame

     # noqa: E501

    :param id: 
    :type id: int

    :rtype: None
    """
    return 'do some magic!'


def get_distance_hd(id):  # noqa: E501
    """Get Distance HD

     # noqa: E501

    :param id: 
    :type id: int

    :rtype: None
    """
    return 'do some magic!'


def get_imageassets(pathImages):  # noqa: E501
    """Get Image assets

     # noqa: E501

    :param pathImages: 
    :type pathImages: int

    :rtype: None
    """
    return 'do some magic!'


def get_polygon_points(id):  # noqa: E501
    """Get Polygon Points

     # noqa: E501

    :param id: 
    :type id: int

    :rtype: None
    """
    return 'do some magic!'


def get_type_analytics():  # noqa: E501
    """Get Type Analytics

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def list_type_analytics():  # noqa: E501
    """List Type Analytics

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def set_distance_hd(id, Body):  # noqa: E501
    """Set Distance HD

     # noqa: E501

    :param id: 
    :type id: int
    :param Body: 
    :type Body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        Body = SetDistanceHDRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def set_polygon_points(id, Body):  # noqa: E501
    """Set Polygon Points

     # noqa: E501

    :param id: 
    :type id: int
    :param Body: 
    :type Body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        Body = SetPolygonPointsRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def set_type_analytics(id, Body):  # noqa: E501
    """Set Type Analytics

     # noqa: E501

    :param id: 
    :type id: int
    :param Body: 
    :type Body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        Body = SetTypeAnalyticsRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
