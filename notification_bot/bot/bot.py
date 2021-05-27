from typing import List

from django.conf import settings

from notification_bot.bot.actions import Bot


def bot(request: dict) -> None:
    vk_bot = Bot()

    event: dict = request['object']['message']
    msg_text: str = event['text'].lower()

    if request['type'] == 'message_new':

        if not message_from_group_chat(event):
            if msg_text == 'подписаться':
                vk_bot.subscribe(event=event)

            elif msg_text == 'отписаться':
                vk_bot.unsubscribe(event=event)

            elif msg_text == 'начать' or msg_text == 'start':
                vk_bot.start(event=event)

        else:
            if vk_bot.was_added_to_chat(event=event):
                if not vk_bot.chat_in_db(peer_id=event['peer_id']):
                    vk_bot.add_new_chat_in_db(peer_id=event['peer_id'])
                vk_bot.help(event=event)

            if msg_text.startswith(f'{settings.BOT_USERNAME}'):
                command_string: str = msg_text.replace(f'{settings.BOT_USERNAME},', '')
                command_string: str = command_string.replace(settings.BOT_USERNAME, '')
                commands_to_bot: List[str] = command_string.split()
                if len(commands_to_bot) != 0:
                    if commands_to_bot[0] == 'подписаться':
                        vk_bot.chat_sub(group=commands_to_bot[1], event=event)

                    elif commands_to_bot[0] == 'отписаться':
                        vk_bot.chat_unsub(group=commands_to_bot[1], event=event)

                    elif commands_to_bot[0] == 'help':
                        vk_bot.help(event=event)

                    elif commands_to_bot[0] == 'подписки':
                        vk_bot.subscribed_to(event=event)
                else:
                    vk_bot.help(event=event)


def message_from_group_chat(event) -> bool:
    return event['peer_id'] >= 2 * 10 ** 9
