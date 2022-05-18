from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render
import httplib2
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.views.generic.list import ListView
from .models import Team
from django.http import JsonResponse
from datetime import date
import os
import pandas as pd
import json



class HomeView(TemplateView):
    template_name = "home.html"

class MapView(TemplateView):
    template_name = "map.html" 

class UsecaseView(TemplateView):
    template_name = "usecase.html"

class Usecase01(TemplateView):
    template_name = "usecase_01.html"

class Usecase02(TemplateView):
    template_name = "usecase_02.html"

class Usecase03(TemplateView):
    template_name = "usecase_03.html"

# class AboutView(TemplateView):
#     template_name = "about.html"

class TeamDetailView(DetailView):
    model = Team
    template_name = 'team-details.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context


class TeamList(ListView):
    context_object_name = 'team_list'
    queryset = Team.objects.all().order_by('id')
    template_name = 'about.html'

#=============== Get Number of Flooded Districts =======================#

# Get latest flooded number of districts of Cambodia
def getCambodiaFloodedDistricts(request):
    df = pd.read_csv('./static/data/cambodia/cambodia_flooded_districts.txt')
    #print(df)
    recent_data = df.tail(1)
    #concatenated = pd.concat([recent_data])
    #print(concatenated)
    json_data = recent_data.to_json(orient='records')
    #print(json)
    return JsonResponse(json_data, safe=False)

# Get latest flooded number of districts of Laos
def getLaosFloodedDistricts(request):
    df = pd.read_csv('./static/data/laos/laos_flooded_districts.txt')
    recent_data = df.tail(1)
    json_data = recent_data.to_json(orient='records')
    return JsonResponse(json_data, safe=False)

# Get latest flooded number of districts of Myanmar
def getMyanmarFloodedDistricts(request):
    df = pd.read_csv('./static/data/myanmar/myanmar_flooded_districts.txt')
    recent_data = df.tail(1)
    json_data = recent_data.to_json(orient='records')
    return JsonResponse(json_data, safe=False)

# Get latest flooded number of districts of Thailand
def getThailandFloodedDistricts(request):
    df = pd.read_csv('./static/data/thailand/thailand_flooded_districts.txt')
    recent_data = df.tail(1)
    json_data = recent_data.to_json(orient='records')
    return JsonResponse(json_data, safe=False)

# Get latest flooded number of districts of Vietnam
def getVietnamFloodedDistricts(request):
    df = pd.read_csv('./static/data/vietnam/vietnam_flooded_districts.txt')
    recent_data = df.tail(1)
    json_data = recent_data.to_json(orient='records')
    return JsonResponse(json_data, safe=False)

## ============ Get Flooded Area ================== */

# Get latest flooded area of Cambodia
def getCambodiaFloodedArea(request):
    df = pd.read_csv('./static/data/cambodia/cambodia_flooded_area.txt')
    #print(df)
    recent_data = df.tail(1)
    #concatenated = pd.concat([recent_data])
    #print(concatenated)
    json_data = recent_data.to_json(orient='records')
    #print(json)
    return JsonResponse(json_data, safe=False)

# Get latest flooded area of Laos
def getLaosFloodedArea(request):
    df = pd.read_csv('./static/data/laos/laos_flooded_area.txt')
    recent_data = df.tail(1)
    json_data = recent_data.to_json(orient='records')
    return JsonResponse(json_data, safe=False)

# Get latest flooded area of Myanmar
def getMyanmarFloodedArea(request):
    df = pd.read_csv('./static/data/myanmar/myanmar_flooded_area.txt')
    recent_data = df.tail(1)
    json_data = recent_data.to_json(orient='records')
    return JsonResponse(json_data, safe=False)

# Get latest flooded area of Thailand
def getThailandFloodedArea(request):
    df = pd.read_csv('./static/data/thailand/thailand_flooded_area.txt')
    recent_data = df.tail(1)
    json_data = recent_data.to_json(orient='records')
    return JsonResponse(json_data, safe=False)

# Get latest flooded area of Vietnam
def getVietnamFloodedArea(request):
    df = pd.read_csv('./static/data/vietnam/vietnam_flooded_area.txt')
    recent_data = df.tail(1)
    json_data = recent_data.to_json(orient='records')
    return JsonResponse(json_data, safe=False)

## ============ Get Number of Flooded Health Center ================== */

# Get latest number of flooded health center of Cambodia
def getCambodiaFloodedHealthCenter(request):
    df = pd.read_csv('./static/data/cambodia/cambodia_flooded_health_center.txt')
    recent_data = df.tail(1)
    json_data = recent_data.to_json(orient='records')
    return JsonResponse(json_data, safe=False)

# Get latest number of flooded health center of Laos
def getLaosFloodedHealthCenter(request):
    df = pd.read_csv('./static/data/laos/laos_flooded_health_center.txt')
    recent_data = df.tail(1)
    json_data = recent_data.to_json(orient='records')
    return JsonResponse(json_data, safe=False)

# Get latest number of flooded health center of Myanmar
def getMyanmarFloodedHealthCenter(request):
    df = pd.read_csv('./static/data/myanmar/myanmar_flooded_health_center.txt')
    recent_data = df.tail(1)
    json_data = recent_data.to_json(orient='records')
    return JsonResponse(json_data, safe=False)

# Get latest number of flooded health center of Thailand
def getThailandFloodedHealthCenter(request):
    df = pd.read_csv('./static/data/thailand/thailand_flooded_health_center.txt')
    recent_data = df.tail(1)
    json_data = recent_data.to_json(orient='records')
    return JsonResponse(json_data, safe=False)

# Get latest number of flooded health center of Vietnam
def getVietnamFloodedHealthCenter(request):
    df = pd.read_csv('./static/data/vietnam/vietnam_flooded_health_center.txt')
    recent_data = df.tail(1)
    json_data = recent_data.to_json(orient='records')
    return JsonResponse(json_data, safe=False)


## ============= Get Number of Flooded Education Center ================ */

# Get latest number of flooded education center of Cambodia
def getCambodiaFloodedEduCenter(request):
    df = pd.read_csv('./static/data/cambodia/cambodia_flooded_education_center.txt')
    recent_data = df.tail(1)
    json_data = recent_data.to_json(orient='records')
    return JsonResponse(json_data, safe=False)

# Get latest number of flooded education center of Laos
def getLaosFloodedEduCenter(request):
    df = pd.read_csv('./static/data/laos/laos_flooded_education_center.txt')
    recent_data = df.tail(1)
    json_data = recent_data.to_json(orient='records')
    return JsonResponse(json_data, safe=False)

# Get latest number of flooded education center of Myanmar
def getMyanmarFloodedEduCenter(request):
    df = pd.read_csv('./static/data/myanmar/myanmar_flooded_education_center.txt')
    recent_data = df.tail(1)
    json_data = recent_data.to_json(orient='records')
    return JsonResponse(json_data, safe=False)

# Get latest number of flooded education center of Thailand
def getThailandFloodedEduCenter(request):
    df = pd.read_csv('./static/data/thailand/thailand_flooded_education_center.txt')
    recent_data = df.tail(1)
    json_data = recent_data.to_json(orient='records')
    return JsonResponse(json_data, safe=False)

# Get latest number of flooded education center of Vietnam
def getVietnamFloodedEduCenter(request):
    df = pd.read_csv('./static/data/vietnam/vietnam_flooded_education_center.txt')
    recent_data = df.tail(1)
    json_data = recent_data.to_json(orient='records')
    return JsonResponse(json_data, safe=False)