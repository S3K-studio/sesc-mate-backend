from typing import Dict, Union, List

import vk_api
from django.conf import settings
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from api.models import User
from notification_bot.messages import Messages
from notification_bot.models import Group, Chat
from utils.group_choices import groups_dict, reversed_groups_defaultdict


class Bot:
    def __init__(self):
        vk_session = vk_api.VkApi(token=settings.VK_BOT_TOKEN)
        vk = vk_session.get_api()

        keyboard_sub = VkKeyboard()
        keyboard_sub.add_button('Подписаться', color=VkKeyboardColor.POSITIVE)

        keyboard_unsub = VkKeyboard()
        keyboard_unsub.add_button('Отписаться', color=VkKeyboardColor.NEGATIVE)

        keyboard_app = VkKeyboard()
        keyboard_app.add_vkapps_button(label='SESC MATE', app_id=7227055, owner_id=186607004, hash='')

        self.vk = vk
        self.keyboard_sub = keyboard_sub
        self.keyboard_unsub = keyboard_unsub
        self.keyboard_app = keyboard_app

    def subscribe(self, event: dict) -> None:
        from_id: int = event['from_id']

        use = self._user_use_app(from_id)

        if use['use']:
            user: User = use['user']
            user_group = user.group
            group_to_sub = Group.objects.get(group_number=user_group)

            if user not in group_to_sub.subscribers.all():
                group_to_sub.subscribers.add(user)
                group_to_sub.save()

                text: str = Messages.YOU_SUB + groups_dict[user_group]
                self.vk.messages.send(
                    peer_id=from_id,
                    random_id=get_random_id(),
                    keyboard=self.keyboard_unsub.get_keyboard(),
                    message=text
                )
            else:
                text: str = Messages.ALREADY_SUB + groups_dict[user_group]
                self.vk.messages.send(
                    peer_id=from_id,
                    random_id=get_random_id(),
                    keyboard=self.keyboard_unsub.get_keyboard(),
                    message=text
                )

        else:
            self.vk.messages.send(
                peer_id=from_id,
                random_id=get_random_id(),
                keyboard=self.keyboard_app.get_keyboard(),
                message=Messages.NOT_USE_APP
            )

    def unsubscribe(self, event: dict) -> None:
        from_id: int = event['from_id']
        use: dict = self._user_use_app(from_id)

        if use['use']:
            user: User = use['user']
            user_group: int = user.group
            group_to_sub: Group = Group.objects.get(group_number=user_group)

            if user in group_to_sub.subscribers.all():
                group_to_sub.subscribers.remove(user)
                group_to_sub.save()

                text: str = Messages.YOU_UNSUB + groups_dict[user_group]
                self.vk.messages.send(
                    peer_id=from_id,
                    random_id=get_random_id(),
                    keyboard=self.keyboard_sub.get_keyboard(),
                    message=text
                )
            else:
                text: str = Messages.ALREADY_UNSUB + groups_dict[user_group]
                self.vk.messages.send(
                    peer_id=from_id,
                    random_id=get_random_id(),
                    keyboard=self.keyboard_sub.get_keyboard(),
                    message=text
                )

        else:
            self.vk.messages.send(
                peer_id=from_id,
                random_id=get_random_id(),
                keyboard=self.keyboard_app.get_keyboard(),
                message=Messages.NOT_USE_APP
            )

    def start(self, event: dict) -> None:
        from_id: int = event['from_id']

        self.vk.messages.send(
            peer_id=from_id,
            random_id=get_random_id(),
            keyboard=self.keyboard_sub.get_keyboard(),
            message=Messages.START
        )

    def chat_sub(self, event: dict, group: str) -> None:
        if reversed_groups_defaultdict[group] is None:
            self.vk.messages.send(
                peer_id=event['peer_id'],
                random_id=get_random_id(),
                message=Messages.GROUP_NOT_EXISTS
            )
        else:
            group_to_sub: Group = Group.objects.get(group_number=reversed_groups_defaultdict[group])
            if group_to_sub not in Chat.objects.get(peer_id=event['peer_id']).subscribed_to.all():
                group_to_sub.chats.add(Chat.objects.get(peer_id=event['peer_id']))
                group_to_sub.save()

                self.vk.messages.send(
                    peer_id=event['peer_id'],
                    random_id=get_random_id(),
                    message=Messages.CHAT_SUBED
                )
            else:
                self.vk.messages.send(
                    peer_id=event['peer_id'],
                    random_id=get_random_id(),
                    message=Messages.ALREADY_SUB_GROUP
                )

    def chat_unsub(self, event: dict, group: str) -> None:
        if reversed_groups_defaultdict[group] is None:
            self.vk.messages.send(
                peer_id=event['peer_id'],
                random_id=get_random_id(),
                message=Messages.GROUP_NOT_EXISTS
            )
        else:
            group_to_unsub: Group = Group.objects.get(group_number=reversed_groups_defaultdict[group])
            if group_to_unsub in Chat.objects.get(peer_id=event['peer_id']).subscribed_to.all():
                group_to_unsub.chats.remove(Chat.objects.get(peer_id=event['peer_id']))
                group_to_unsub.save()

                self.vk.messages.send(
                    peer_id=event['peer_id'],
                    random_id=get_random_id(),
                    message=Messages.CHAT_UNSUBED
                )
            else:
                self.vk.messages.send(
                    peer_id=event['peer_id'],
                    random_id=get_random_id(),
                    message=Messages.NOT_SUB_GROUP
                )

    def help(self, event: dict) -> None:
        self.vk.messages.send(
            peer_id=event['peer_id'],
            random_id=get_random_id(),
            message=Messages.HELP
        )

    @staticmethod
    def was_added_to_chat(event: dict) -> bool:
        return (
                'action' in event and
                event['action']['type'] == 'chat_invite_user' and
                event['action']['member_id'] == - settings.VK_GROUP_ID
        )

    @staticmethod
    def remove_chat(chats_ids: List[int]) -> None:
        for chat in chats_ids:
            Chat.objects.get(peer_id=chat).delete()

    @staticmethod
    def remove_users(user_ids: List[int]) -> None:
        for user_id in user_ids:
            user = User.objects.get(vk_user_id=user_id)
            group_to_unsub = Group.objects.get(group_number=user.group)
            group_to_unsub.subscribers.remove(user)
            group_to_unsub.save()

    @staticmethod
    def split_sends_info(info: List[dict]) -> Dict[str, list]:
        unsubs = [receiver['peer_id'] for receiver in info if 'error' in receiver.keys()]

        chats_to_del = []
        users_to_del = []
        for unsub_id in unsubs:
            if unsub_id >= 2 * 10 ** 9:
                chats_to_del.append(unsub_id)
            else:
                users_to_del.append(unsub_id)

        return {'chats': chats_to_del, 'users': users_to_del}

    def subscribed_to(self, event: dict) -> None:
        chat = Chat.objects.get(peer_id=event['peer_id'])
        subscribed_to = []
        for group in chat.subscribed_to.all():
            group_number = group.group_number
            subscribed_to.append(groups_dict[group_number])

        if len(subscribed_to) == 0:
            self.vk.messages.send(
                peer_id=event['peer_id'],
                random_id=get_random_id(),
                message=Messages.SUBLIST_EMPTY
            )

        else:
            self.vk.messages.send(
                peer_id=event['peer_id'],
                random_id=get_random_id(),
                message=Messages.you_sub_on(group_list=subscribed_to)
            )

    @staticmethod
    def add_new_chat_in_db(peer_id: int) -> None:
        chat = Chat.objects.create(peer_id=peer_id)
        chat.save()

    @staticmethod
    def chat_in_db(peer_id: int) -> bool:
        try:
            Chat.objects.get(peer_id=peer_id)
            return True

        except Chat.DoesNotExist:
            return False

    @staticmethod
    def _user_use_app(user_id: int) -> dict:
        try:
            user: User = User.objects.get(vk_user_id=user_id)
            resp: Dict[str, Union[bool, User]] = {
                'use': True,
                'user': user
            }
        except User.DoesNotExist:
            resp: Dict[str, Union[bool, User]] = {
                'use': False,
            }
        return resp
