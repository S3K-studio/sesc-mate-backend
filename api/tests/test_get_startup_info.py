from typing import List, Any
from unittest.mock import patch

from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.serializers import UserSerializer
from utils import generate_vk_headers
from utils.announcements_mock import AnnouncementsMock
from utils.get_mocked_schedule import get_schedule


def get_announcements(*args) -> List[Any]:
    announcements_mock = AnnouncementsMock()
    return announcements_mock.get_annoucements_mock()


class GetStartupInfoTest(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('startup-info')
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

    @patch('api.views.get_parsed_announcements', get_announcements)
    @patch('api.views.get_parsed_schedule', get_schedule)
    def test_get_startup_info(self):
        data = {
            'day': 1
        }
        valid_response_data = {
            'success': True,
            'setupCompleted': True,
            'groupId': self.user_group,
            'timetable': get_schedule(),
            'announcements': get_announcements()
        }
        vk_headers = generate_vk_headers.generate_vk_headers(self.vk_user_id,
                                                             settings.CLIENT_SECRET_KEY)
        response = self.client.get(self.url, data, **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, valid_response_data)

    def test_get_startup_info_schedule_mock(self):
        data = {
            'day': 1,
            'schedule_mock': ''
        }
        vk_headers = generate_vk_headers.generate_vk_headers(12345, settings.CLIENT_SECRET_KEY)
        response = self.client.get(self.url, data, **vk_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
