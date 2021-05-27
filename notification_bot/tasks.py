from hashlib import sha1
from datetime import datetime, timedelta

import vk_api
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.cache import cache
from vk_api.keyboard import VkKeyboard
from vk_api.utils import get_random_id
from typing import List

from api.services.cache import get_parsed_schedule
from notification_bot.models import Group
from sesc_mate.celery import app
from utils.days_choices import days_dict_for_link
from utils.group_choices import groups_dict
from .bot.bot import Bot
from .messages import Messages

logger = get_task_logger(__name__)
GROUP_IDS = list(groups_dict.keys())


@app.task
def check_schedule_for_changes() -> str:
    """Task для celery, проверяющий изменилось ли расписание для каждого класса и дня"""

    bot = Bot()
    for group in GROUP_IDS:
        for day in range(1, 7):
            key = get_schedule_cache_key(day, group)
            logger.info('fetching schedule for {}'.format(key))
            try:
                schedule_now: str = compute_hash(str(get_parsed_schedule(day, group, force_update=True)))
                existing_schedule: str = cache.get(key)
                cache.set(key, schedule_now, timeout=1200)

                if skip_notification(day):
                    continue

                if existing_schedule is not None:
                    if schedule_now != existing_schedule:
                        logger.info('broadcasting changes ({} -> {})'.format(existing_schedule, schedule_now))

                        ids_for_sending = []
                        for user in Group.objects.get(group_number=group).subscribers.all():
                            ids_for_sending.append(user.vk_user_id)

                        for chat in Group.objects.get(group_number=group).chats.all():
                            ids_for_sending.append(chat.peer_id)

                        sends_info = send_message(ids_for_sending, group, day)

                        split_data = bot.split_sends_info(sends_info)
                        chats_to_del, users_to_del = split_data['chats'], split_data['users']

                        bot.remove_chat(chats_to_del)
                        bot.remove_users(users_to_del)

                else:
                    logger.warn('cache is not set, skipping')

            except Exception as e:
                logger.exception(e)
                return str(e)

    return 'OKAY'


def get_schedule_cache_key(weekday: int, group: int) -> str:
    """Возвращает ключ для хранения закэшированного расписания"""

    return f"bot_schedule_weekday{weekday}_group{group}"


def send_message(vk_ids: List[int], group: int, day: int) -> List[dict]:
    """Отправляет собщение с ссылкой на измененное расписание"""

    try:
        vk_session = vk_api.VkApi(token=settings.VK_BOT_TOKEN)
        vk = vk_session.get_api()

        inline_keyboard = VkKeyboard(inline=True)
        inline_keyboard.add_vkapps_button(label='Посмотреть',
                                          app_id=7227055,
                                          owner_id=settings.VK_GROUP_ID,
                                          hash=f"s-{group}-{days_dict_for_link[day]}")

        return vk.messages.send(
            peer_ids=vk_ids,
            random_id=get_random_id(),
            message=Messages.create_notification_message(group, day),
            keyboard=inline_keyboard.get_keyboard()
        )

    except Exception as e:
        print(e)
        return []


def skip_notification(changed_day: int) -> bool:
    today = (datetime.today() + timedelta(hours=5)).weekday()
    if today == 7:
        return False
    return changed_day < today


def compute_hash(payload: str) -> str:
    return sha1(payload.encode()).hexdigest()
