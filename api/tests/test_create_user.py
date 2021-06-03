import json

from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from utils import generate_vk_headers


class CreateUserTest(APITestCase):
    def test_valid_user_create(self):
        url = reverse('user')
        data = {
            'group': 32
        }
        vk_user_id = 12345
        vk_headers = generate_vk_headers.generate_vk_headers(vk_user_id, settings.CLIENT_SECRET_KEY)
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['vk_user_id'], vk_user_id)
        self.assertEqual(response.data['group'], data['group'])

    def test_invalid_user_create(self):
        url = reverse('user')
        data = {
            'group': 32
        }
        vk_headers = generate_vk_headers.generate_vk_headers(12345, settings.CLIENT_SECRET_KEY,
                                                             False)
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
