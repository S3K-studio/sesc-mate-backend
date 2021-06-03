from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.serializers import UserSerializer
from utils import generate_vk_headers


class DeleteUserTest(APITestCase):
    def setUp(self):
        self.vk_user_id = 12345
        self.user_group = 32
        user_data = {
            'vk_user_id': self.vk_user_id,
            'group': self.user_group,
            'first_name': 'first_name',
            'last_name': 'last_name',
            'sex': 2,
            'profile_picture_url': ''
        }
        serializer = UserSerializer()
        serializer.create(validated_data=user_data)

    def test_valid_user_delete(self):
        url = reverse('user')
        response_valid_data = {
            'vk_user_id': self.vk_user_id,
            'group': self.user_group
        }
        vk_headers = generate_vk_headers.generate_vk_headers(12345, settings.CLIENT_SECRET_KEY)
        response = self.client.delete(url, data={}, **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_valid_data)

    def test_invalid_user_delete(self):
        url = reverse('user')
        vk_headers = generate_vk_headers.generate_vk_headers(12345, settings.CLIENT_SECRET_KEY,
                                                             False)
        response = self.client.delete(url, data={}, **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
