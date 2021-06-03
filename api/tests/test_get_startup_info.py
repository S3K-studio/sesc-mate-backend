from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from utils import generate_vk_headers


class GetStartupInfoTest(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('startup-info')

    def test_get_startup_info(self):
        data = {
            'day': 1
        }
        vk_headers = generate_vk_headers.generate_vk_headers(12345, settings.CLIENT_SECRET_KEY)
        response = self.client.get(self.url, data, **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_startup_info_schedule_mock(self):
        data = {
            'day': 1,
            'schedule_mock': ''
        }
        vk_headers = generate_vk_headers.generate_vk_headers(12345, settings.CLIENT_SECRET_KEY)
        response = self.client.get(self.url, data, **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
