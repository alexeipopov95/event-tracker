# -*- coding: utf8 -*-
"""
POST /api/events/{EVENT_NAME}/{NUM}  => increase N times the ocurrencies of an event 
"""



#django
from django.http import JsonResponse, HttpResponse
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


class UpdateEventCounter(View):
    content_type = "application/json"


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateEventCounter, self).dispatch(request, *args, **kwargs)


    def create_history(self, event, _request):
        """
        Method designed for creating a new value in EventHistory table
        """

        #capture the request and parse it to save into details the request data
        detail = {
            'content_type' : _request.content_type,
            'headers'      : _request.headers,
            'method'       : _request.method,
            'path'         : _request.path,
        }

        # if exist in META "REMOTE_ADD" save it as the ip address where the request come from
        if _request.META.get('REMOTE_ADDR'):
            ip_address = _request.META.get('REMOTE_ADDR')
            detail['ip_address'] = ip_address

        try:
            history = EventHistory.objects.create(
                name=event,
                detail=detail,
                creation_date = datetime.now()
            )
            history.save()
        except expression as CreationHistoryException:
            print(CreationHistoryException)



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
            #first instance i check if the event type exist
            event_type = EventType.objects.get(name=str(kwargs['event_name']))

            try:
                #if exist i try to get the event
                event, created = Event.objects.get_or_create(
                    event = event_type,
                    creation_date__date=datetime.today().date()
                )

                #if created for the first time on the day i set the creation date and the counter value
                if created:
                    event.counter       = kwargs['value']
                    event.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.create_history(event=event, _request=request)
                    response['response'] = 201
                
                #else, just increase the existing one
                else:
                    event.counter = event.counter + kwargs['value']
                    self.create_history(event=event, _request=request)
                    response['response'] = 204
                
                event.save()

                response['status'] = True

            except Exception as GetOrCreateException:
                response['response'] = 404
                response['error']['internal'] = GetOrCreateException.__str__()
                response['error']['external'] = "Something went wrong"
            
        except Exception as PostResponseException:
            response['response'] = 404
            response['error']['internal'] = PostResponseException.__str__()
            response['error']['external'] = "Something went wrong"

        return JsonResponse(response)

