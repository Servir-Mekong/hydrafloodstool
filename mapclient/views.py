from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render
import httplib2
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.views.generic.list import ListView
from .models import Team

class HomeView(TemplateView):
    template_name = "home.html"

class MapView(TemplateView):
    template_name = "map.html" 

class UsecaseView(TemplateView):
    template_name = "usecase.html"

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
