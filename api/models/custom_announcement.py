from django.db import models


class CustomAnnouncement(models.Model):
    header = models.CharField(max_length=120, unique=False)
    content = models.TextField()
    is_pinned = models.BooleanField(default=False)
