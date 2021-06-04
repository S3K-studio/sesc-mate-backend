from utils.days_choices import days_dict_for_message
from utils.group_choices import groups_dict
from utils.days_choices import days_dict_for_alice
from utils.group_choices import reversed_groups_defaultdict, groups_dict
from api.services.cache import get_parsed_schedule

from typing import Union
import pymorphy2
from datetime import datetime, timedelta


class Messages:
    START = {
        'text': 'Привет, это sesc mate, попроси меня запомнить твой класс, или спроси расписание',
        'tts': 'Привет, это sesc mate, попроси меня запомнить твой класс, или спроси расписание'
    }

    UNEXISTING_GROUP = {
        'text': 'К сожалению, такого класса нет',
        'tts': 'К сожалению, такого класса нет'
    }

    NO_GROUP = {
        'text': 'Я не знаю вашего класса',
        'tts': 'Я не знаю вашего класса',
    }

    def schedule_message(self, raw_day: str, group: Union[str, int]) -> dict:
        if isinstance(group, str):
            raw_group = group
            group_number = reversed_groups_defaultdict[group]
        else:
            group_number = group
            raw_group = groups_dict[group]

        day_number = self.__get_day_number_(raw_day)
        if day_number == 7:
            text = 'В воскресенье вообще-то выходной'
        else:
            schedule = get_parsed_schedule(day_number, group_number)
            # schedule = get_parsed_schedule(day_number, group_number, fake=1)
            print(schedule)
            if day_number == 1:
                text_first_part = f'В понедельник у {raw_group} '
            elif day_number == 2:
                text_first_part = f'Во вторник у {raw_group} '
            elif day_number == 3:
                text_first_part = f'В среду у {raw_group} '
            elif day_number == 4:
                text_first_part = f'В четверг у {raw_group} '
            elif day_number == 5:
                text_first_part = f'В пятницу у {raw_group} '
            else:
                text_first_part = f'В субботу у {raw_group} '

            if len(schedule) == 0:
                text_second_part = 'нет уроков'
            else:
                text_second_part = 'будет '
                for lesson in schedule:
                    if isinstance(lesson, list):
                        lesson.sort(key=lambda x: x['subgroup'])
                        group1 = lesson[0]
                        group2 = lesson[1]
                        text_second_part += f'{group1["subject"]} у первой подгруппы '
                        text_second_part += f'{group2["subject"]} у второй подгруппы '
                    else:
                        text_second_part += lesson['subject'] + ' '

            text = text_first_part + text_second_part

        text_tts = {
            'text': text,
            'tts': text
        }
        return text_tts

    @staticmethod
    def you_set_group(group: str):
        text = f'Отлично, теперь ваш класс {group}'

        text_tts = {
            'text': text,
            'tts': text
        }
        return text_tts

    @staticmethod
    def __get_day_number_(raw_day):
        morph = pymorphy2.MorphAnalyzer(lang='ru')

        normal_form = morph.parse(raw_day)[0].normal_form

        if normal_form == 'завтра':
            return (datetime.utcnow() + timedelta(days=1, hours=5)).weekday() + 1
        elif normal_form == 'послезавтра':
            return (datetime.utcnow() + timedelta(days=2, hours=5)).weekday() + 1
        else:
            return days_dict_for_alice[normal_form]
