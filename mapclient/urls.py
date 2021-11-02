from django.urls import path
from . import views, api
from django.conf.urls import include, url
#from oauth2client.contrib.django_util.site import urls as oauth2_urls

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('map/', views.MapView.as_view(), name='mapviewer'),
    path('usecase/', views.UsecaseView.as_view(), name='usecase'),
    path('api/', api.api, name='api-data'),
    url(r'^ajax/date/$', api.dateList),
    url(r'^ajax/floodmap/$', api.api),
]