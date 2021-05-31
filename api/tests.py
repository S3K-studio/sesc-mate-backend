import json
from base64 import b64encode
from collections import OrderedDict
from hashlib import sha256
from hmac import HMAC
from urllib.parse import urlencode

from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestSchedule(APITestCase):
    def test_get_schedule(self):
        url = reverse('get-schedule')
        data = {
            'day': 1,
            'group': 32
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestWeekSchedule(APITestCase):
    def test_get_week_schedule(self):
        url = reverse('get-week-schedule')
        data = {
            'group': 32
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUser(APITestCase):
    def test_user_create(self):
        vk_subset = OrderedDict([('vk_access_token_settings', 'notify'), ('vk_app_id', '7227055'),
                                 ('vk_are_notifications_enabled', '0'), ('vk_is_app_user', '1'),
                                 ('vk_is_favorite', '1'), ('vk_language', 'ru'),
                                 ('vk_platform', 'desktop_web'), ('vk_ref', 'other'),
                                 ('vk_ts', '1614515174'), ('vk_user_id', '12345')])
        hash_code = b64encode(
            HMAC(settings.CLIENT_SECRET_KEY.encode(), urlencode(vk_subset, doseq=True).encode(),
                 sha256).digest())
        sign = hash_code.decode('utf-8')[:-1].replace('+', '-').replace('/', '_')
        vk_subset['sign'] = sign
        vk_headers = {'HTTP_X_VK_DATA': '&'.join(
            ['{}={}'.format(item, vk_subset[item]) for item in vk_subset])}
        url = reverse('user')
        data = {
            'group': 32
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
