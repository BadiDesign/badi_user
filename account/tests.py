# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

from badi_user.api.api import AuthViewSet
from badi_user.models import Token
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from rest_framework.authentication import SessionAuthentication
from rest_framework.test import RequestsClient
import json
from rest_framework.test import APIRequestFactory, APITestCase
from product.api.view_sets import *
from product.models import *
from core.settings import *
import os

os.environ["SMS__ENABLE"] = ""


class AuthRestTestCase(APITestCase):

    def setUp(self):
        print('Start To Test APIs')
        os.environ["SMS__ENABLE"] = ""
        print('Setup Done!')

    def test_login(self):
        print('--------------------------------')
        print('Start to test Auth ViewSet:')

        url = '/api/v1/auth/register/'
        send_sms = self.client.post(
            url,
            {
                'mobile_number': '09390444542',
                'password': '09390444542',
                'first_name': 'mohammad',
                'last_name': 'shekari',
                'is_seller': 'on',
                'is_buyer': 'on',
            },
            format='json'
        )
        self.assertEqual(send_sms.status_code, 200)
        self.assertIsNotNone(send_sms.data.get('token', None))
        print('Send Token:     Success.')

        token = Token.objects.last()
        register = self.client.post(
            url,
            {
                'token': token.token,
                'mobile_number': '09390444542',
                'password': '09390444542',
                'first_name': 'mohammad',
                'last_name': 'shekari',
                'is_seller': 'on',
                'is_buyer': 'on',
            },
            format='json'
        )
        self.assertEqual(register.status_code, 200)
        self.assertIsNotNone(register.data.get('access', None))
        print('Register:       Success.')

        url = '/api/v1/auth/login/'
        response = self.client.post(
            url, {
                'username': '09390444542',
                'password': '09390444542',
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.token_key = 'Bearer ' + response.data.get('access')

        self.client.credentials(Authorization=self.token_key)
        print('Login:          Success.')

        url = '/api/v1/member/self/'
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, 200)
        print('Self:           Success.')
