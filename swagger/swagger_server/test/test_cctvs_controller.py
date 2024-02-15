# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestCctvsController(BaseTestCase):
    """CctvsController integration test stubs"""

    def test_cctvs(self):
        """Test case for cctvs

        Cctvs
        """
        response = self.client.open(
            '//cctvs',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_cctv(self):
        """Test case for create_cctv

        Create Cctv
        """
        data = dict(link_rtsp='link_rtsp_example',
                    name='name_example',
                    location='location_example',
                    ip='ip_example',
                    username='username_example',
                    password='password_example')
        response = self.client.open(
            '//cctvs/create',
            method='POST',
            data=data,
            content_type='application/x-www-form-urlencoded')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_cctv(self):
        """Test case for delete_cctv

        Delete Cctv
        """
        response = self.client.open(
            '//cctvs/{id}'.format(id=56),
            method='DELETE',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_detail_cctv(self):
        """Test case for detail_cctv

        Detail Cctv
        """
        response = self.client.open(
            '//cctvs/{id}'.format(id=56),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_cctv(self):
        """Test case for update_cctv

        Update Cctv
        """
        data = dict(link_rtsp='link_rtsp_example',
                    name='name_example',
                    location='location_example',
                    ip='ip_example',
                    username='username_example',
                    password='password_example')
        response = self.client.open(
            '//cctvs/{id}'.format(id=56),
            method='PUT',
            data=data,
            content_type='application/x-www-form-urlencoded')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
