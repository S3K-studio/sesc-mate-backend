from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class GetScheduleTest(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('get-schedule')

    def test_get_schedule(self):
        data = {
            'day': 1,
            'group': 32
        }
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_schedule_mock(self):
        data = {
            'day': 1,
            'group': 32,
            'schedule_mock': ''
        }
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
