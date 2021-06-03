import json
import os
from typing import List, Dict


class AnnouncementsMock:
    announcements_mock: List[Dict]

    def __init__(self):
        self.announcements_mock = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AnnouncementsMock, cls).__new__(cls)
        return cls.instance

    def get_annoucements_mock(self) -> List[Dict]:
        if self.announcements_mock:
            return self.announcements_mock

        current_dir = os.path.dirname(__file__)
        announcements_mock_json_path = os.path.join(current_dir, 'announcements_mock.json')

        with open(announcements_mock_json_path, 'r', encoding='utf-8') as announcements:
            self.announcements_mock = json.load(announcements)
        return self.announcements_mock


if __name__ == '__main__':
    first_object = AnnouncementsMock()
    second_object = AnnouncementsMock()
    print(first_object, second_object, first_object == second_object)
