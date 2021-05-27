from django.conf import settings
from requests import get


def verify_server(token, base_url, group_id, server_id):
    response = get(
        'https://api.vk.com/method/groups.editCallbackServer',
        params={
            'group_id': group_id,
            'access_token': token,
            'v': '5.130',
            'url': base_url + '/api/v2/bot/',
            'title': 'SESC MATE',
            'secret_key': settings.BOT_SECRET_KEY,
            'server_id': server_id
        }
    )

    return response.json()
