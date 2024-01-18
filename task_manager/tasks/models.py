from django.db import models
from django.utils.translation import gettext as _
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):

    name = models.CharField(
        max_length=150,
        blank=False,
        unique=True,
        verbose_name=_('Name')
    )

    description = models.TextField(
        blank=True,
        verbose_name=_('description')
    )

    creation_date = models.DateTimeField(
        auto_now_add=True
    )

    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author',
        verbose_name=_('author')
    )

    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='status',
        verbose_name=_('status')
    )

    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='executor',
        verbose_name=_('Executor')
    )

    labels = models.ManyToManyField(
        Label,
        through='TaskLabel',
        through_fields=('task', 'label'),
        blank=True,
        related_name='labels',
        verbose_name=_('Labels')
    )

    def __str__(self):
        return self.name


class TaskLabel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
