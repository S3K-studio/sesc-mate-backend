from utils.days_choices import days_dict_for_message
from utils.group_choices import groups_dict


class Messages:
    NOT_USE_APP = 'Вы еще не зарегистрированы в приложении:( Нажмите на кнопку снизу!'
    ALREADY_SUB = 'Вы уже подписаны на уведомления '
    YOU_SUB = 'Вы подписались на уведомления '
    YOU_UNSUB = 'Вы отписались от уведомлений '
    ALREADY_UNSUB = 'Вы не подписаны на уведомления '
    START = 'Привет, здесь ты можешь подписаться на уведомления об изменениях расписания!'
    GROUP_NOT_EXISTS = 'Такого класса не существует'
    CHAT_SUBED = 'Вы подписались'
    CHAT_UNSUBED = 'Вы отписались'
    HELP = 'Привет, вот команды, которые ты можешь написать:\n' \
           '\"@sescmate, подписаться 11н\" - подписаться на уведомления об изменениях расписания класса\n' \
           '\"@sescmate, отписаться 11н\" - отписаться от уведомлений об изменениях расписания класса\n' \
           '\"@sescmate, help\" - узнать команды\n' \
           '\"@sescmate, подписки\" - узнать на какие классы подписана эта беседа\n'
    SUBLIST_EMPTY = 'Вы ни на что не подписаны('
    NOT_SUB_GROUP = 'Вы не подписаны на этот класс'
    ALREADY_SUB_GROUP = 'Вы уже подписаны на этот класс'

    @staticmethod
    def create_notification_message(group: int, day_number: int) -> str:
        message = f'Изменилось расписание на {days_dict_for_message[day_number]} для {groups_dict[group]}'
        return message

    @staticmethod
    def you_sub_on(group_list) -> str:
        message = 'Вы подписаны на:\n'
        groups = '\n'.join(group_list)
        return message + groups

