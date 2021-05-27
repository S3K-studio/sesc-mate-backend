from django.core.cache import cache
from django.conf import settings
from typing import List, Dict
import json

from ..data_from_sesc import get_schedule
from ..parser import ScheduleParser


def _get_schedule_cache_key(weekday: int, group: int) -> str:
    """Получить ключ для хранения закэшированного расписания"""
    return f"schedule_weekday{weekday}_group{group}"


def get_parsed_schedule(weekday: int, group: int, force_update: bool = False) -> List[List[Dict]]:
    """Получить закешированное расписание для класса на день недели"""
    key = _get_schedule_cache_key(weekday, group)
    schedule = cache.get(key)
    if force_update or schedule is None:  # Если нет расписания в кэше
        sesc_schedule = get_schedule(weekday, group)
        sesc_json = json.loads(sesc_schedule)
        schedule = ScheduleParser(sesc_json).get_lessons()
        cache.set(key, schedule, settings.NEWS_CACHE_TTL)
    return schedule
