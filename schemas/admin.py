#Django
from django.contrib import admin

#Custom
from schemas.models.event import Event
from schemas.models.event_type import EventType
from schemas.models.event_history import EventHistory




@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Event model admin, displays the fields in the admin page
    """


    list_display = (
    'event_name',
    'creation_date',
    'counter',
    )

    def event_name(self, obj):
        """ obj is an instance of the selected element in the admin panel. """

        return obj.event.name
        event_name.short_description = "Evento"




@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    """
    EventType model admin, displays the fields in the admin page
    """

    list_display = (
    'name',
    'creation_date',
    'is_active',
    'description',
    )



@admin.register(EventHistory)
class EventHistoryAdmin(admin.ModelAdmin):
    """
    EventHistory model admin, displays the fields in the admin page
    """

    list_display = (
        'event_name',
        'creation_date'
    )

    def event_name(self, obj):
        """ obj is an instance of the selected element in the admin panel. """

        return obj.name.event.name
        event_name.short_description = "Evento"