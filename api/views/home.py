# -*- coding: utf8 -*-
"""
GET /api/events/histogram/{EVENT}/{YYYMMDD} => return a PNG/JPG file with a histogram chart showing the frecuency for a given event
Response:
        - chartjs 
"""

#django
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "index.html"