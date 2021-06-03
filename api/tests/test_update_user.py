import json

from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.serializers import UserSerializer
from utils import generate_vk_headers


class UpdateUserTest(APITestCase):
    def setUp(self):
        self.vk_user_id = 12345
        self.user_group = 22
        user_data = {
            'vk_user_id': self.vk_user_id,
            'group': 32,
            'first_name': 'first_name',
            'last_name': 'last_name',
            'sex': 2,
            'profile_picture_url': ''
        }
        serializer = UserSerializer()
        serializer.create(validated_data=user_data)
        self.data = {
            'group': self.user_group
        }

    def test_valid_user_update(self):
        url = reverse('user')
        response_valid_data = {
            'vk_user_id': self.vk_user_id,
            'group': self.user_group
        }
        vk_headers = generate_vk_headers.generate_vk_headers(12345, settings.CLIENT_SECRET_KEY)
        response = self.client.put(url, data=json.dumps(self.data), content_type='application/json',
                                   **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_valid_data)

    def test_invalid_user_update(self):
        url = reverse('user')
        vk_headers = generate_vk_headers.generate_vk_headers(12345, settings.CLIENT_SECRET_KEY,
                                                             False)
        response = self.client.put(url, data=json.dumps(self.data), content_type='application/json',
                                   **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
