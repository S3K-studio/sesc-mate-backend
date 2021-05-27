import json

import requests
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from notification_bot.bot.bot import bot


@csrf_exempt
def index(request) -> HttpResponse:
    """Вызывается при получении запроса от бота вк"""

    try:
        request: dict = json.loads(request.body.decode('utf-8'))
        if request['secret'] == settings.BOT_SECRET_KEY:

            if request["type"] == "confirmation" and request["group_id"] == settings.VK_GROUP_ID:
                return HttpResponse(get_code())

            bot(request)
            return HttpResponse('ok')

        else:
            return HttpResponse('fuck u')

    except Exception as e:
        return HttpResponse('Error')


def get_code() -> str:
    """Возращает код авторизации сервера для бота вк"""

    url: str = "https://api.vk.com/method/groups.getCallbackConfirmationCode"
    key: str = requests.get(
        url,
        params={
            'group_id': settings.VK_GROUP_ID,
            'access_token': settings.VK_BOT_TOKEN,
            'v': '5.130'
        }
    ).json()['response']['code']

    return key
