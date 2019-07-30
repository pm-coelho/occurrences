from django.db import models
from django.conf import settings
from enum import Enum

# TODO: localization


class State(Enum):
    NOT_VALIDATED = 'not validated'
    VALIDATED = 'validated'
    RESOLVED = 'resolved'


class Category(Enum):
    CONSTRUCTION = 'planned road work'
    SPECIAL_EVENT = 'special events (fair, sport event, etc.)'
    INCIDENT = 'accidents and other unexpected events'
    WHEATHER_CONDITION = 'weather condition affecting the road'
    ROAD_CONDITION = 'status of the road that might affect travellers \
    (potholes, bad pavement, etc)'


class Occurrence(models.Model):
    description = models.CharField(max_length=255)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    state = models.CharField(
        max_length=20,
        choices=[(tag.name, tag.value) for tag in State]
    )
    category = models.CharField(
        max_length=20,
        choices=[(tag.name, tag.value) for tag in Category]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description
