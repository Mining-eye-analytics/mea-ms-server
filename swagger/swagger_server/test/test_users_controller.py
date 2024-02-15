# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestUsersController(BaseTestCase):
    """UsersController integration test stubs"""

    def test_check_username(self):
        """Test case for check_username

        Check Username
        """
        response = self.client.open(
            '//users/{username}/exists'.format(username='username_example'),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_user(self):
        """Test case for delete_user

        Delete User
        """
        response = self.client.open(
            '//users/{id}'.format(id=56),
            method='DELETE',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_detail_user(self):
        """Test case for detail_user

        Detail User
        """
        response = self.client.open(
            '//users/{id}'.format(id=56),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login(self):
        """Test case for login

        Login
        """
        headers = [('Authorization', 'Bearer {token}')]
        data = dict(username='username_example',
                    password='password_example')
        response = self.client.open(
            '//users/login',
            method='POST',
            headers=headers,
            data=data,
            content_type='application/x-www-form-urlencoded')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_register(self):
        """Test case for register

        Register
        """
        headers = [('Authorization', 'Bearer {token}')]
        data = dict(company='company_example',
                    full_name='full_name_example',
                    username='username_example',
                    role='role_example',
                    password='password_example')
        response = self.client.open(
            '//users/create',
            method='POST',
            headers=headers,
            data=data,
            content_type='application/x-www-form-urlencoded')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_user(self):
        """Test case for update_user

        Update User
        """
        data = dict(company='company_example',
                    full_name='full_name_example',
                    username='username_example',
                    role='role_example')
        response = self.client.open(
            '//users/{id}'.format(id=56),
            method='PUT',
            data=data,
            content_type='application/x-www-form-urlencoded')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_users(self):
        """Test case for users

        Users
        """
        response = self.client.open(
            '//users',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
