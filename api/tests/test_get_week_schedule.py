from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from utils.get_mocked_schedule import get_schedule


class GetWeekScheduleTest(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('get-week-schedule')

    @patch('api.views.get_parsed_schedule', get_schedule)
    def test_get_week_schedule(self):
        data = {
            'group': 32
        }
        valid_response_data = [get_schedule()] * 6
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, valid_response_data)

    def test_get_week_schedule_mock(self):
        data = {
            'day': 1,
            'group': 32,
            'schedule_mock': ''
        }
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
