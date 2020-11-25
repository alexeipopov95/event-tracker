# -*- coding: utf8 -*-
"""
GET /api/events?start_date=YYYYMMDDHH&end_date=YYYYMMDD  => list all the events between START_DATE and END_DATE 

Response:
{
[{'date':'2020091112','event':'login','count':12}],
[{'date':'2020091113','event':'login','count':2000}],
[{'date':'2020091114','event':'login','count':5400}],
[{'date':'2020091112','event':'resource/209','count':1}],
[{'date':'2020091113','event':'resource/209','count':203}],
[{'date':'2020091114','event':'resource/209','count':33}]
}

"""
#django
from django.http import JsonResponse
from django.views.generic import View

#custom
from schemas.models.event import Event

#python
from datetime import datetime
import json

class EventStats(View):
    content_type = "application/json"


    def convert_to_datetime(self, values):
        """
        A method designed for parsing the income dates from params and convert them into datetime format
        """
        start, end = values
        try:
            start, end = values
            start = datetime.strptime(str(start), '%Y%m%d%H')
            end = datetime.strptime(str(end), '%Y%m%d')

        except Exception as DatetimeConverterException:
            print(DatetimeConverterException)

        return (start, end)


    def get(self, request):
        """
        get method for handling requests, process them and return a JSON Response
        """
        response = {
            'status'   : False,
            'response' : {},
            'error' : {
                'internal' : None,
                'external' : None,
            }
        }

        try:
            start_date = int(request.GET.get('start_date'))
            end_date   = int(request.GET.get('end_date'))

            start, end = self.convert_to_datetime((start_date, end_date))

            if len(str(start_date)) == 10 and len(str(end_date)) == 8:

                if start > end:
                    response['error']['internal'] = "start_date is higher than end_date"
                    response['error']['external'] = "Back to the future?"
                    return JsonResponse(response)

                _range  = [
                    "%s" % start,
                    "%s" % end.replace(hour=23, minute=59, second=59)
                ]

                events_list = []
                events = Event.objects.filter(creation_date__range=_range)

                for value in events:
                    record = {}
                    try:
                        record['date']  = value.creation_date.strftime("%Y%m%d%H")
                        record['event'] = value.event.name
                        record['count'] = value.counter
                        events_list.append([record])
                    except Exception as EventIterException:
                        print(EventIterException)

                response['status']   = True
                response['response'] = events_list

            else:
                response['error']['internal'] = "Invalid format for start_date or end_date, length must be 10 and 8 respectively"
                response['error']['external'] = "Invalid date format"
                return JsonResponse(response)


        except Exception as ParamGetException:
            response['error']['internal'] = ParamGetException.__str__()
            response['error']['external'] = "Please give a valid date values"
            




        return JsonResponse(response)