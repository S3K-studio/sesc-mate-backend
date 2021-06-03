from django.db import models


class AliceUser(models.Model):
    group_number = models.IntegerField(default=0)
    user_id = models.TextField()

    def __str__(self):
        return f'id: {self.id}, group: {self.group_number}'

    def __repr__(self):
        return f'id: {self.id}, group: {self.group_number}'
