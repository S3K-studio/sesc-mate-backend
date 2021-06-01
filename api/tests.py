import json

from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.serializers import UserSerializer
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


class CreateUserTest(APITestCase):
    def test_valid_user_create(self):
        url = reverse('user')
        data = {
            'group': 32
        }
        vk_headers = generate_vk_headers.generate_vk_headers(12345, settings.CLIENT_SECRET_KEY)
        response = self.client.post(url, data=json.dumps(data), content_type='application/json',
                                    **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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
        user_data = {
            'vk_user_id': 12345,
            'group': 32,
            'first_name': 'first_name',
            'last_name': 'last_name',
            'sex': 2,
            'profile_picture_url': ''
        }
        serializer = UserSerializer()
        serializer.create(validated_data=user_data)

    def test_valid_user_get(self):
        url = reverse('user')
        vk_headers = generate_vk_headers.generate_vk_headers(12345, settings.CLIENT_SECRET_KEY)
        response = self.client.get(url, data={}, **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_user_get(self):
        url = reverse('user')
        vk_headers = generate_vk_headers.generate_vk_headers(12345, settings.CLIENT_SECRET_KEY,
                                                             False)
        response = self.client.get(url, data={}, **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateUserTest(APITestCase):
    def setUp(self):
        user_data = {
            'vk_user_id': 12345,
            'group': 32,
            'first_name': 'first_name',
            'last_name': 'last_name',
            'sex': 2,
            'profile_picture_url': ''
        }
        serializer = UserSerializer()
        serializer.create(validated_data=user_data)
        self.data = {
            'group': 22
        }

    def test_valid_user_update(self):
        url = reverse('user')
        vk_headers = generate_vk_headers.generate_vk_headers(12345, settings.CLIENT_SECRET_KEY)
        response = self.client.put(url, data=json.dumps(self.data), content_type='application/json',
                                   **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_user_update(self):
        url = reverse('user')
        vk_headers = generate_vk_headers.generate_vk_headers(12345, settings.CLIENT_SECRET_KEY,
                                                             False)
        response = self.client.put(url, data=json.dumps(self.data), content_type='application/json',
                                   **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteUserTest(APITestCase):
    def setUp(self):
        user_data = {
            'vk_user_id': 12345,
            'group': 32,
            'first_name': 'first_name',
            'last_name': 'last_name',
            'sex': 2,
            'profile_picture_url': ''
        }
        serializer = UserSerializer()
        serializer.create(validated_data=user_data)

    def test_valid_user_delete(self):
        url = reverse('user')
        vk_headers = generate_vk_headers.generate_vk_headers(12345, settings.CLIENT_SECRET_KEY)
        response = self.client.delete(url, data={}, **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_user_delete(self):
        url = reverse('user')
        vk_headers = generate_vk_headers.generate_vk_headers(12345, settings.CLIENT_SECRET_KEY,
                                                             False)
        response = self.client.delete(url, data={}, **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
