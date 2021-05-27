from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.group_choices import GROUP_CHOICES
from utils.sex_choices import SEX_CHOICES


class User(AbstractUser):
    """Модель ученика"""
    username = models.CharField(max_length=64, unique=False)
    vk_user_id = models.BigIntegerField(null=True, blank=True, unique=True)  # id пользователя в вк
    group = models.IntegerField(choices=GROUP_CHOICES, null=True, blank=True)  # класс пользователя
    profile_picture_url = models.CharField(max_length=512, blank=True, null=True)  # URL на аватарку пользователя
    sex = models.IntegerField(choices=SEX_CHOICES, default=0)  # пол пользователя

    USERNAME_FIELD = 'vk_user_id'
    REQUIRED_FIELDS = ['username', 'group']

    def __str__(self) -> str:
        return "{0} {1} - {2}"\
            .format(self.first_name, self.last_name,
                    next(filter(lambda user_group: user_group[0] == self.group, GROUP_CHOICES), None)[1])

    def __repr__(self) -> str:
        return f'User(vk_user_id={self.vk_user_id}, group={self.group})'

    def get_grade(self) -> int:
        """Получить цифру класса, в котором учится пользователь"""
        return int(self.get_group_display()[:-1])

    def get_profile_picture_tag(self) -> str:
        return '<img src="{}" width="32" height="32" style="border-radius: 64px" />'\
            .format(self.profile_picture_url or 'https://vk.com/images/camera_50.png')

    def get_vk_link_tag(self) -> str:
        return '<a target="_blank" href="https://vk.com/id{}" class="inlineviewlink">{}</a>'\
            .format(self.vk_user_id, self.vk_user_id)
