# -*- coding: utf-8 -*-
#from celery.result import AsyncResult
from . core import MainGEEApi
from django.conf import settings
from django.http import JsonResponse
from datetime import date, datetime
import ee, json, os, time

# def api(request):

#     get = request.GET.get
#     action = get('action', '')

#     if action:
#         public_methods = ['get-map-id', 'get-permanent-water', 'get-precipmap', 'get-date-list']#'download-flood-map', 'get-feeds-data'
#         if action in public_methods:
#             date = get('date', '')
#             shape = get('shape', '')
#             geom = get('geom', '')
            #fcolor = get('fcolor', '')
            #sensor = get('sensor', '')
            #startYear = get('startYear', '')
            #endYear = get('endYear', '')
            #startMonth = get('startMonth', '')
            #endMonth = get('endMonth', '')
            #method = get('method', '')
            #wcolor = get('wcolor', '')
            #accum = get('accum', '')
            #cmap = get('cmap', '')
            #precipdate = get('precipdate', '')
            #core = GEEApi(date, shape, geom ) #sensor, fcolor
            #if action == 'get-map-id':
            #    data = core.get_map_id(date=date, shape=geom) #sensor=sensor,fcolor=fcolor, 
            #elif action == 'get-permanent-water':
            #    data = core.getHistoricalMap(startYear=startYear, endYear=endYear, startMonth=startMonth, endMonth=endMonth, method=method, wcolor=wcolor, climatology=False, algorithm='JRC', shape=geom)
            #elif action == 'get-precipmap':
            #   data = core.getPrecipMap(date=precipdate, accumulation=1, cmap_name=cmap)     
            #elif action == 'get-date-list':
            #    data = core.dateList()
            #elif action == 'get-feeds-data':
            #    data = core.getFeeds()
            #elif action == 'download-flood-map':
            #    download_date = get('download_date', '')
                #download_snsr = get('download_snsr', '')
            #    download_shape = get('download_shape', '')
            #    data = core.getDownloadURL(download_date, download_shape)#download_snsr,
            #return JsonResponse(data, safe=False)


def dateList(request):
    if request.is_ajax and request.method == "GET":
        core = MainGEEApi(date)
        data = core.dateList()
        return JsonResponse(data, safe=False)

def api(request):
    if request.is_ajax and request.method == "GET": 
        core = MainGEEApi(date)
        data = core.get_map_id()
        return JsonResponse(data, safe=False)