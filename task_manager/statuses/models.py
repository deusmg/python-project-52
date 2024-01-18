from django.db import models
from django.utils.translation import gettext as _


class Status(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        unique=True,
        verbose_name=_('Name')
    )
    creation_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
