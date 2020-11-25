from django.utils.translation import gettext as _
from django.db import models

from schemas.models.event import Event


class EventHistory(models.Model):
    """ EventHistory model, designed to log every request into a designed event, it depends of the Event model """

    name          = models.ForeignKey(Event, on_delete=models.CASCADE ,verbose_name=_("Event"))
    detail        = models.TextField(verbose_name=_("Detail"), blank=True, null=True)
    creation_date = models.DateTimeField(verbose_name=_("Creation Date"), auto_now_add=False, blank=True, null=True)

    class Meta:
        app_label = 'schemas'
        verbose_name = _("History")
        verbose_name_plural = _("History")

    def __str__(self):
        return "{0}".format(self.name.event.name)
