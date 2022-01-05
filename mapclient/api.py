# -*- coding: utf-8 -*-
#from celery.result import AsyncResult
from . core import MainGEEApi
from django.conf import settings
from django.http import JsonResponse
from datetime import date, datetime
import ee, json, os, time
from ee.ee_exception import EEException
from django.views.decorators.csrf import csrf_exempt

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


# def dateList(request):
#     if request.is_ajax and request.method == "GET":
#         core = MainGEEApi(date)
#         data = core.dateList()
#         return JsonResponse(data, safe=False)

# def api(request):
#     if request.is_ajax and request.method == "GET": 
#         core = MainGEEApi(date)
#         data = core.get_map_id()
#         return JsonResponse(data, safe=False)
#Get date list
def dateList(request):
    if request.is_ajax and request.method == "GET":
        #core = MainGEEApi(date)
        core = MainGEEApi()
        data = core.getDateList()
        return JsonResponse(data, safe=False)

#Get precipitation map
@csrf_exempt
def get_precipitation_map(request):
    if request.is_ajax and request.method == "GET": 
        date = request.GET.get('selected_date')
        cmap = request.GET.get('cmap')
        accum = request.GET.get('accum')
        core = MainGEEApi()
        data = core.getPrecipMap(date, accumulation=accum, cmap_name=cmap)
        return JsonResponse(data, safe=False)

#Get daily surface water map
@csrf_exempt
def get_dailysurface_water_map(request):
    if request.is_ajax and request.method == "GET":
        date = request.GET.get('selected_date')        
        core = MainGEEApi()
        data = core.getFloodMap(date)
        return JsonResponse(data, safe=False)

#Get permanent water map
@csrf_exempt
def get_permanent_water_map(request):
    if request.is_ajax and request.method == "GET":
        startYear = request.GET.get('startYear')
        endYear = request.GET.get('endYear')
        startMonth = request.GET.get('startMonth')
        endMonth = request.GET.get('endMonth')
        method = request.GET.get('method')
        core = MainGEEApi()
        data = core.getHistoricalMap(startYear, endYear, startMonth, endMonth, method, climatology=False, algorithm='JRC')#, shape=geom , wcolor=wcolor,
        return JsonResponse(data, safe=False)

def get_download_url(request):
    if request.is_ajax and request.method == "GET":
        date = request.GET.get('selected_date', '')
        shape = request.GET.get('geom', '')
        core = MainGEEApi()
        data = core.getDownloadURL(date, shape)
    return JsonResponse(data, safe=False)

