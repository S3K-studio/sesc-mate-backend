from typing import List, Dict

from utils.schedule_mock import ScheduleMock


def get_schedule(*args) -> List[List[Dict]]:
    schedule_mock = ScheduleMock()
    return [schedule_mock.get_schedule_mock()]
