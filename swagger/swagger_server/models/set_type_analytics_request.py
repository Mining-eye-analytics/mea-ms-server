# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class SetTypeAnalyticsRequest(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, type_analytics: str=None):  # noqa: E501
        """SetTypeAnalyticsRequest - a model defined in Swagger

        :param type_analytics: The type_analytics of this SetTypeAnalyticsRequest.  # noqa: E501
        :type type_analytics: str
        """
        self.swagger_types = {
            'type_analytics': str
        }

        self.attribute_map = {
            'type_analytics': 'type_analytics'
        }

        self._type_analytics = type_analytics

    @classmethod
    def from_dict(cls, dikt) -> 'SetTypeAnalyticsRequest':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SetTypeAnalyticsRequest of this SetTypeAnalyticsRequest.  # noqa: E501
        :rtype: SetTypeAnalyticsRequest
        """
        return util.deserialize_model(dikt, cls)

    @property
    def type_analytics(self) -> str:
        """Gets the type_analytics of this SetTypeAnalyticsRequest.


        :return: The type_analytics of this SetTypeAnalyticsRequest.
        :rtype: str
        """
        return self._type_analytics

    @type_analytics.setter
    def type_analytics(self, type_analytics: str):
        """Sets the type_analytics of this SetTypeAnalyticsRequest.


        :param type_analytics: The type_analytics of this SetTypeAnalyticsRequest.
        :type type_analytics: str
        """
        if type_analytics is None:
            raise ValueError("Invalid value for `type_analytics`, must not be `None`")  # noqa: E501

        self._type_analytics = type_analytics
