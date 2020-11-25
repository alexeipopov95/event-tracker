# -*- coding: utf8 -*-

"""
GET /api/events/unique => list all the events stored historically
Response:
{
[{'event':'login','count':7512}],
[{'event':'resource/209','count':237}],
}

[
    [{'event': 'login', 'count': 978}],
    [{'event': 'resource/209', 'count': 59}]
]
"""

#django
from django.http import JsonResponse
from django.views.generic import View

#custom
from schemas.models.event_type import EventType
from schemas.models.event import Event

#python
from datetime import datetime
import json

class UniqueEvent(View):
    content_type = "application/json"


    def event_processor(self, _events):
        """
        abstract method for event processing
        - Expects a <list>
        """

        event_list = []
        #iter a list of event names
        for event_name in _events:
            counter = {}
            try:
                #filter events in Events table by event name
                events_queryset = Event.objects.filter(event__name=event_name)
                counter['event'] = event_name
                counter['count'] = 0

                #django querysets is better to count with native counter instead of len()
                if events_queryset.count() > 0:

                    #iter the objects instances and increase the counter
                    for query in events_queryset:
                        counter['count'] = counter['count'] + query.counter

    
                event_list.append([counter])

            except Exception as EventFilterException:
                print(EventFilterException)
        
        return event_list


    def get(self, request, *arg, **kwargs):
        """
        get method for handling requests, process them and return a JSON Response
        """
        response = {
            'status'   : False,
            'response' : {},
            'error'    : {
                'internal' : None,
                'external' : None
            }
        }

        try:
            #list comprehencion querying a low values table for names
            events = [event.name for event in EventType.objects.filter(is_active=True)]

            events = self.event_processor(_events=events)

            response['status']   = True
            response['response'] = events


        except Exception as GetException:
            response['error']['internal'] = GetException.__str__()
            response['error']['external'] = "Something went wrong"
        
        return JsonResponse(response)

        