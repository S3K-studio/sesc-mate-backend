from django.core.cache import cache
from typing import List, Any

from ..data_from_sesc import get_announcements
from ..parser import AnnouncementsParser


def _get_announcements_cache_key() -> str:
    """Получить ключ для хранения закэшированных объявлений"""
    return "announcements"


def get_parsed_announcements(force_update: bool = False) -> List[Any]:
    """Получить закэшированные объявления"""
    key = _get_announcements_cache_key()
    announcements = cache.get(key)
    if force_update or announcements is None:  # Если нет объявлений в кэше
        sesc_announcements_html = get_announcements()
        announcements = AnnouncementsParser(sesc_announcements_html).parse()
        cache.set(key, announcements, None)
    return announcements
