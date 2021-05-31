from base64 import b64encode
from collections import OrderedDict
from hashlib import sha256
from hmac import HMAC
from typing import Dict
from urllib.parse import urlencode


def generate_vk_headers(vk_user_id: int, secret: str) -> Dict[str, str]:
    vk_subset = OrderedDict([('vk_access_token_settings', 'notify'), ('vk_app_id', '7227055'),
                             ('vk_are_notifications_enabled', '0'), ('vk_is_app_user', '1'),
                             ('vk_is_favorite', '1'), ('vk_language', 'ru'),
                             ('vk_platform', 'desktop_web'), ('vk_ref', 'other'),
                             ('vk_user_id', str(vk_user_id))])
    hash_code = b64encode(
        HMAC(secret.encode(), urlencode(vk_subset, doseq=True).encode(),
             sha256).digest())
    sign = hash_code.decode('utf-8')[:-1].replace('+', '-').replace('/', '_')
    vk_subset['sign'] = sign
    vk_headers = {'HTTP_X_VK_DATA': '&'.join(
        ['{}={}'.format(item, vk_subset[item]) for item in vk_subset])}
    return vk_headers
