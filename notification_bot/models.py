from __future__ import unicode_literals

from django.db import models

from utils.group_choices import GROUP_CHOICES
from api.models.user import User


class Chat(models.Model):
    peer_id = models.IntegerField()

    def __str__(self):
        return f'peer_id: {self.peer_id}'

    def __repr__(self):
        return f'peer_id: {self.peer_id}'


class Group(models.Model):
    group_number = models.IntegerField(choices=GROUP_CHOICES)
    subscribers = models.ManyToManyField(User, related_name='subscribed_to')
    chats = models.ManyToManyField(Chat, related_name='subscribed_to')

    def __str__(self):
        return f'group_number: {self.group_number}, subscribers: {self.subscribers}'

    def __repr__(self):
        return f'group_number: {self.group_number}, subscribers: {self.subscribers}'
