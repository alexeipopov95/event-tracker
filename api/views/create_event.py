# -*- coding: utf8 -*-
"""
POST /api/events/{EVENT_NAME} => count an ocurrency of an event
"""


#django
from django.http import JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


#custom
from schemas.models.event_type import EventType
from schemas.models.event import Event
from schemas.models.event_history import EventHistory

#python
from datetime import datetime
import json


class CreateEvent(View):
    content_type = "application/json"


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateEvent, self).dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):

        response = {
            'status' : False,
            'response' : None,
            'error' : {
                'internal' : None,
                'external' : None
            }
        }


        try:
            if kwargs['event_name']:
                event_name = kwargs['event_name']

                #lookup for the event type in the EventType table if it exist or no
                event, created = EventType.objects.get_or_create(
                    name=event_name
                )

                if created:

                    #optional if you want to pass a short description about the event
                    if request.POST.get('desc'):
                        event.description = request.POST.get('desc')
                    else:
                        event.description = "Event created by automatic script"
                    event.save()

                    #the status will be true and the status code will be 201 (created)
                    response['status']   = True
                    response['response'] = 201

                else:
                    #the status will be true but the response is going to be a 403 (already exists)
                    response['status']   = True
                    response['response'] = 403
            
            else:
                response['response'] = "Wrong url param"
            
        except expression as EventCreator:
            response['error']['internal'] = EventCreator.__str__()
            response['error']['external'] = "Something went wrong"

        return JsonResponse(response)

