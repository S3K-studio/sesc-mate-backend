import json

from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from utils import generate_vk_headers


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
        url = reverse('user')
        data = {
            'group': 32
        }
        vk_headers = generate_vk_headers.generate_vk_headers(12345, settings.CLIENT_SECRET_KEY)
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
