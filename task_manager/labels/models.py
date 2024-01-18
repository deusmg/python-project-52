from django.db import models
from django.utils.translation import gettext as _


class Label(models.Model):

    name = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        verbose_name=_('Name')
    )

    creation_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
