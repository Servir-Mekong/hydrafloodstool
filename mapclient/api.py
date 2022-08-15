# -*- coding: utf-8 -*-
# from celery.result import AsyncResult
from . core import MainGEEApi
from django.conf import settings
from django.http import JsonResponse
from datetime import date, datetime
import ee, json, os, time
from ee.ee_exception import EEException
from django.views.decorators.csrf import csrf_exempt

# Get date list
# def dateList(request):
#     if request.is_ajax and request.method == "GET":
#         #core = MainGEEApi(date)
#         core = MainGEEApi()
#         data = core.getDateList()
#         return JsonResponse(data, safe=False)

# Get precipitation map
@csrf_exempt
def get_precipitation_map(request):
    if request.is_ajax and request.method == "GET": 
        date = request.GET.get('selected_date')
        cmap = request.GET.get('cmap')
        accum = request.GET.get('accum')
        core = MainGEEApi()
        data = core.getPrecipMap(date, accumulation=accum, cmap_name=cmap)
        return JsonResponse(data, safe=False)

# Get potential flood map
def get_potential_flood_map(request):
    if request.is_ajax and request.method == "GET":
        start_date = request.GET.get('selected_start_date')
        end_date = request.GET.get('selected_end_date') 
        #adm =  request.GET.get('selected_adm') 
        sensor =  request.GET.get('selected_sensor')  
        mode =  request.GET.get('selected_mode')  
        ops_date = request.GET.get('ops_date')
        core = MainGEEApi()
        data = core.getPotentialFloodMap(start_date, end_date, mode, sensor, ops_date) #adm,
        return JsonResponse(data, safe=False)

# Get daily surface water map
@csrf_exempt
def get_dailysurface_water_map(request):
    if request.is_ajax and request.method == "GET":
        date = request.GET.get('selected_date') 
        sensor =  request.GET.get('sensor')       
        core = MainGEEApi()
        data = core.getSurfaceWaterMap(date, sensor)
        return JsonResponse(data, safe=False)

# Get flood age map
@csrf_exempt
def get_flood_age_map(request):
    if request.is_ajax and request.method == "GET":
        age_date = request.GET.get('age_date')  
        # age_type =  request.GET.get('selected_age_type') 
        age_sensor =  request.GET.get('selected_age_sensor')   
        core = MainGEEApi()
        data = core.getFloodAgeMap(age_date, age_sensor)
        return JsonResponse(data, safe=False)

# Get flood duration map
@csrf_exempt
def get_flood_duration_map(request):
    if request.is_ajax and request.method == "GET":
        # date = request.GET.get('selected_date')        
        core = MainGEEApi()
        data = core.getFloodDurationMap()
        return JsonResponse(data, safe=False)


# Get permanent water map
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
        date = request.GET.get('selected_date')
        adm =  request.GET.get('adm_selection')
        core = MainGEEApi()
        data = core.getDownloadURL(date, adm)
    return JsonResponse(data, safe=False)

def get_case_flood_map(request):
    if request.is_ajax and request.method == "GET":
        date = request.GET.get('selected_date')
        core = MainGEEApi()
        data = core.getCaseFloodMap(date)
    return JsonResponse(data, safe=False)

def get_jrc_permanent_water_map(request):
    if request.is_ajax:
        core = MainGEEApi()
        data = core.getJRCPermanentWaterMap()
    return JsonResponse(data, safe=False)

def get_doy_map(request):
    if request.is_ajax and request.method == "GET":
        start_date = request.GET.get('selected_start_date')
        end_date = request.GET.get('selected_date')
        # selected_region = request.GET.get('selected_region')
        core = MainGEEApi()
        data = core.getDOYMap(start_date, end_date)
    return JsonResponse(data, safe=False)

def get_eel_map(request):
    if request.is_ajax:
        core = MainGEEApi()
        data = core.getEELMap()
    return JsonResponse(data, safe=False)
