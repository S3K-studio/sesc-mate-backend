from typing import List, Dict
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from utils.schedule_mock import ScheduleMock


def get_schedule(*args) -> List[List[Dict]]:
    schedule_mock = ScheduleMock()
    return [schedule_mock.get_schedule_mock()]


class GetScheduleTest(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('get-schedule')

    @patch('api.views.get_parsed_schedule', get_schedule)
    def test_get_schedule(self):
        data = {
            'day': 1,
            'group': 32
        }
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, get_schedule())

    def test_get_schedule_mock(self):
        data = {
            'day': 1,
            'group': 32,
            'schedule_mock': ''
        }
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
