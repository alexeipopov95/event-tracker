# -*- coding: utf8 -*-
"""
GET /api/events/histogram/{EVENT}/{YYYMMDD} => return a PNG/JPG file with a histogram chart showing the frecuency for a given event
Response:
        - chartjs 
"""

#django
from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse


#Custom
from schemas.models.event_history import EventHistory

#python
from collections import Counter
from datetime import datetime
import pandas as pd
import json

class Histogram(TemplateView):
    template_name = "histogram.html"


class HistogramDataView(View):

    def formater(self, queryset, date):

        final = {k:0 for k in range(24)}

        try:
            data = []

            for label in queryset:
                data.append(label.creation_date.hour)

            data = dict(Counter(data))
            final.update(data)

        except Exception as FormaterException:
            print(FormaterException)

        return final
    

    def chart_color(self):
        try:
            colors = ["rgb(102, 102, 255)" for _ in range(24)]
        except expression as ChartColorException:
            print(ChartColorException)
        return colors



    def get(self, request, *args, **kwargs):

        context = {}
        chart_labels = []
        chart_events = []

        try:
            #date
            if type(kwargs['datetime']) is int and len(str(kwargs['datetime'])) == 8:
                date = datetime.strptime(str(kwargs['datetime']), "%Y%m%d")

                date_range  = [
                "{0}".format(date.replace(hour=0, minute=0, second=0)),
                "{0}".format(date.replace(hour=23, minute=59, second=59))
                ]

                try:
                    history = EventHistory.objects.filter(
                        name__event__name=kwargs['event_name'],
                        creation_date__range=date_range
                    )
                    chart = self.formater(history, date)
                    for keys, values in chart.items():
                        chart_labels.append(keys)
                        chart_events.append(values)
                    
                    context['chart_labels'] = chart_labels
                    context['chart_events'] = chart_events
                    context['chart_colors'] = self.chart_color()


                except Exception as FindValuesException:
                    print(FindValuesException)
            else:
                return HttpResponseBadRequest("<h1>Bad Parameters</h1>")

        except Exception as InvalidDateFormat:
            print(InvalidDateFormat)


        
        return JsonResponse(context)