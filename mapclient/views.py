from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render
import httplib2

class HomeView(TemplateView):
    template_name = "home.html"

class MapView(TemplateView):
    template_name = "map.html" 

class UsecaseView(TemplateView):
    template_name = "usecase.html"


# @oauth_required
# def index(request):

#     oauth = request.oauth
#     try:
#         oauth.credentials.get_access_token(httplib2.Http())
#     except Exception as e:
#         oauth.get_authorize_redirect()

#     return render(request, 'map.html', {})

    
    
