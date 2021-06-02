import json
import os
from typing import List, Dict


class ScheduleMock:
    schedule_mock: List[Dict]

    def __init__(self):
        self.schedule_mock = []

    def get_schedule_mock(self) -> List[Dict]:
        if self.schedule_mock:
            return self.schedule_mock

        current_dir = os.path.dirname(__file__)
        schedule_mock_json_path = os.path.join(current_dir, 'schedule_mock.json')

        with open(schedule_mock_json_path, 'r', encoding='utf-8') as schedule:
            self.schedule_mock = json.load(schedule)
        return self.schedule_mock
