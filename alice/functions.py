from .models import AliceUser

from typing import Dict, Union


def create_response(text_tts: dict, end: bool):
    text = text_tts['text']
    tts = text_tts['tts']
    response = {
        "response": {
            "text": text,
            "tts": tts,
            "end_session": end
        },
        "version": "1.0"
    }

    return response


def is_new_user(user_id: str) -> dict:
    try:
        user = AliceUser.objects.get(user_id=user_id)
        response: Dict[str, Union[bool, int]] = {
            'new': False,
            'group_number': user.group_number
        }
    except AliceUser.DoesNotExist:
        response: Dict[str, Union[bool, int]] = {
            'new': True,
        }
    return response


def user_has_group(user_id: str) -> Union[bool, int]:
    user = AliceUser.objects.get(user_id=user_id)
    return user.group_number
