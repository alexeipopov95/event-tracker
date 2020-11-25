from django.utils.translation import gettext as _
from django.db import models
from schemas.models.event_type import EventType

# Create your models here.

class Event(models.Model):
    """ Event model, depends on a EventType model and it is in charge of creating the daily values """

    event         = models.ForeignKey(EventType, on_delete=models.CASCADE, verbose_name=_("Event"))
    creation_date = models.DateTimeField(verbose_name=_("Creation date"), auto_now_add=True)
    counter       = models.PositiveIntegerField(verbose_name=_("Counter"), blank=True, null=True, default=0)

    class Meta:
        app_label = 'schemas'
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self):
        return "{0}".format(self.event.name)