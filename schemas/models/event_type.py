from django.utils.translation import gettext as _
from django.db import models

class EventType(models.Model):
    """ EventType model, in charge of creating the different types of events """

    name          = models.CharField(verbose_name=_("Event"), max_length=255, blank=True, null=True)
    description   = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    creation_date = models.DateTimeField(verbose_name=_("Creation date"), auto_now_add=True)
    is_active     = models.BooleanField(verbose_name=_("Active"), default=True)
    

    class Meta:
        app_label = 'schemas'
        verbose_name = _("Event type")
        verbose_name_plural = _("Event types")

    def __str__(self):
        return "{0}".format(self.name)