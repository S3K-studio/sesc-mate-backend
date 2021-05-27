import requests

SESC_DOMAIN = "lyceum.urfu.ru"


def get_schedule(weekday: int, group: int) -> str:
    """Получить json расписания с сервера СУНЦа"""
    return requests.get(f"https://{SESC_DOMAIN}/?type=11&scheduleType=group&weekday={weekday}&group={group}").text


def get_news() -> str:
    """Получить html новостей с сервера СУНЦа"""
    return requests.get(f"https://{SESC_DOMAIN}/news").text


def get_announcements() -> str:
    """Получить html объявлений с сервера СУНЦа"""
    return requests.get(f"https://{SESC_DOMAIN}/dopolnitelnye-stranicy/objavlenija").text
