import json

from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.serializers import UserSerializer
from utils import generate_vk_headers


class ScheduleTest(APITestCase):
    def test_get_schedule(self):
        url = reverse('get-schedule')
        data = {
            'day': 1,
            'group': 32
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WeekScheduleTest(APITestCase):
    def test_get_week_schedule(self):
        url = reverse('get-week-schedule')
        data = {
            'group': 32
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetStartupInfoTest(APITestCase):
    def test_get_startup_info(self):
        url = reverse('startup-info')
        data = {
            'day': 1
        }
        vk_headers = generate_vk_headers.generate_vk_headers(12345, settings.CLIENT_SECRET_KEY)
        response = self.client.get(url, data, **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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


class GetUserTest(APITestCase):
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

    def test_valid_user_get(self):
        url = reverse('user')
        response_valid_data = {
            'vk_user_id': self.vk_user_id,
            'group': self.user_group
        }
        vk_headers = generate_vk_headers.generate_vk_headers(12345, settings.CLIENT_SECRET_KEY)
        response = self.client.get(url, data={}, **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, response_valid_data)

    def test_invalid_user_get(self):
        url = reverse('user')
        vk_headers = generate_vk_headers.generate_vk_headers(12345, settings.CLIENT_SECRET_KEY,
                                                             False)
        response = self.client.get(url, data={}, **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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
