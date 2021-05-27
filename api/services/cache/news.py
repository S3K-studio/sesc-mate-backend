from django.core.cache import cache
from django.conf import settings
from typing import List, Any

from ..data_from_sesc import get_news
from ..parser import NewsParser


def _get_news_cache_key() -> str:
    """Получить ключ для хранения закэшированных новостей"""
    return "news"


def get_parsed_news(force_update: bool = False) -> List[Any]:
    """Получить закэшированные новости"""
    key = _get_news_cache_key()
    news = cache.get(key)
    if force_update or news is None:  # Если нет объявлений в кэше
        sesc_news_html = get_news()
        news = NewsParser(sesc_news_html).parse()
        cache.set(key, news, settings.NEWS_CACHE_TTL)
    return news
