from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class GetWeekScheduleTest(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('get-week-schedule')

    def test_get_week_schedule(self):
        data = {
            'group': 32
        }
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_week_schedule_mock(self):
        data = {
            'day': 1,
            'group': 32,
            'schedule_mock': ''
        }
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
