# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestDeviationsController(BaseTestCase):
    """DeviationsController integration test stubs"""

    def test_detail_realtime_deviations(self):
        """Test case for detail_realtime_deviations

        Detail Realtime Deviations
        """
        response = self.client.open(
            '//deviations/{id}'.format(id=56),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_detail_realtime_images(self):
        """Test case for detail_realtime_images

        Detail Realtime Images
        """
        response = self.client.open(
            '//deviations/ri/{id}'.format(id=56),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_deviations(self):
        """Test case for deviations

        Deviations
        """
        query_string = [('cctv_id', 56),
                        ('filter_notification', 'filter_notification_example'),
                        ('type_object', 'type_object_example'),
                        ('limit', 56)]
        response = self.client.open(
            '//deviations/v1',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_deviationswith_child(self):
        """Test case for deviationswith_child

        Deviations with Child
        """
        query_string = [('cctv_id', 56),
                        ('filter_notification', 'filter_notification_example'),
                        ('type_object', 'type_object_example'),
                        ('limit', 56)]
        response = self.client.open(
            '//deviations/v2',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_type_object(self):
        """Test case for list_type_object

        List Type Object
        """
        response = self.client.open(
            '//deviations/list-type-object',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_realtime_deviations(self):
        """Test case for realtime_deviations

        Realtime Deviations
        """
        response = self.client.open(
            '//deviations',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_realtime_images(self):
        """Test case for realtime_images

        Realtime Images
        """
        response = self.client.open(
            '//deviations/ri',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_realtime_deviations(self):
        """Test case for update_realtime_deviations

        Update Realtime Deviations
        """
        data = dict(type_validation=true,
                    comment='comment_example',
                    user_id=56)
        response = self.client.open(
            '//deviations/{id}'.format(id=56),
            method='PUT',
            data=data,
            content_type='application/x-www-form-urlencoded')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
