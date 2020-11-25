from django.urls import path

from api.views.get_list import UniqueEvent
from api.views.get_stats import EventStats
from api.views.event_add_count import UpdateEventCounter
from api.views.create_event import CreateEvent
from api.views.get_histogram import Histogram, HistogramDataView

urlpatterns = [
    #list all historic events in the database
    path('events/unique/', UniqueEvent.as_view(), name="unique" ),

    #list events between 2 dates // Params: start_date: YYYYMMDDHH & end_date: YYYYMMDD
    path('events/', EventStats.as_view(), name="stats" ),

    #create event_type
    path('events/<str:event_name>/', CreateEvent.as_view(), name="create-event" ),

    #update an existing event
    path('events/<str:event_name>/<int:value>', UpdateEventCounter.as_view(), name='update-counter'),


    #Histogram    
    path('events/histogram/<str:event_name>/<int:datetime>/', Histogram.as_view(), name="histogram" ),
    path('events/histogram/json/<str:event_name>/<int:datetime>/', HistogramDataView.as_view(), name="json_histogram" ),


]
