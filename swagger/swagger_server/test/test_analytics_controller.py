# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.set_distance_hd_request import SetDistanceHDRequest  # noqa: E501
from swagger_server.models.set_polygon_points_request import SetPolygonPointsRequest  # noqa: E501
from swagger_server.models.set_type_analytics_request import SetTypeAnalyticsRequest  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAnalyticsController(BaseTestCase):
    """AnalyticsController integration test stubs"""

    def test_generate_frame(self):
        """Test case for generate_frame

        Generate Frame
        """
        response = self.client.open(
            '//analytics/{id}/video_feed'.format(id=56),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_distance_hd(self):
        """Test case for get_distance_hd

        Get Distance HD
        """
        response = self.client.open(
            '//analytics/{id}/distance_hd'.format(id=56),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_imageassets(self):
        """Test case for get_imageassets

        Get Image assets
        """
        response = self.client.open(
            '//analytics/{pathImage}'.format(pathImages=56),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_polygon_points(self):
        """Test case for get_polygon_points

        Get Polygon Points
        """
        response = self.client.open(
            '//analytics/{id}/polygon'.format(id=56),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_type_analytics(self):
        """Test case for get_type_analytics

        Get Type Analytics
        """
        response = self.client.open(
            '//analytics/{id}/type_analytics',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_type_analytics(self):
        """Test case for list_type_analytics

        List Type Analytics
        """
        response = self.client.open(
            '//analytics/list',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_distance_hd(self):
        """Test case for set_distance_hd

        Set Distance HD
        """
        Body = SetDistanceHDRequest()
        response = self.client.open(
            '//analytics/{id}/distance_hd'.format(id=56),
            method='POST',
            data=json.dumps(Body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_polygon_points(self):
        """Test case for set_polygon_points

        Set Polygon Points
        """
        Body = SetPolygonPointsRequest()
        response = self.client.open(
            '//analytics/{id}/polygon'.format(id=56),
            method='POST',
            data=json.dumps(Body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_type_analytics(self):
        """Test case for set_type_analytics

        Set Type Analytics
        """
        Body = SetTypeAnalyticsRequest()
        response = self.client.open(
            '//analytics/{id}/type_analytics'.format(id=56),
            method='POST',
            data=json.dumps(Body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
