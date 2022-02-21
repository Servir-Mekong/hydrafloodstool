from django.urls import path
from . import views, api
from django.conf.urls import include, url
#from oauth2client.contrib.django_util.site import urls as oauth2_urls

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('map/', views.MapView.as_view(), name='mapviewer'),
    path('usecase/', views.UsecaseView.as_view(), name='usecase'),
    #path('about/', views.AboutView.as_view(), name='about'),
    path('about/', views.TeamList.as_view(), name='about'),
    path('people/<slug:slug>/', views.TeamDetailView.as_view(), name='team-detail'),
    url(r'^ajax/date/$', api.dateList),
    url(r'^ajax/precipmap/$', api.get_precipitation_map),
    url(r'^ajax/potentialfloodmap/$', api.get_potential_flood_map),
    url(r'^ajax/surfacewatermap/$', api.get_dailysurface_water_map),
    url(r'^ajax/permanaentwatermap/$', api.get_permanent_water_map),
    url(r'^ajax/downloadfloodmap/$', api.get_download_url),
    url(r'^ajax/casefloodmap/$', api.get_case_flood_map),
    url(r'^ajax/jrcpermanentwatermap/$', api.get_jrc_permanent_water_map),
    url(r'^ajax/cambodiafloodedarea/$', views.getCambodiaFloodedArea),
    url(r'^ajax/laosfloodedarea/$', views.getLaosFloodedArea),
    url(r'^ajax/myanmarfloodedarea/$', views.getMyanmarFloodedArea),
    url(r'^ajax/thailandfloodedarea/$', views.getThailandFloodedArea),
    url(r'^ajax/vietnamfloodedarea/$', views.getVietnamFloodedArea),

    url(r'^ajax/cambodiafloodedhealthcenter/$', views.getCambodiaFloodedHealthCenter),
    url(r'^ajax/laosfloodedhealthcenter/$', views.getLaosFloodedHealthCenter),
    url(r'^ajax/myanmarfloodedhealthcenter/$', views.getMyanmarFloodedHealthCenter),
    url(r'^ajax/thailandfloodedhealthcenter/$', views.getThailandFloodedHealthCenter),
    url(r'^ajax/vietnamfloodedhealthcenter/$', views.getVietnamFloodedHealthCenter),
    url(r'^ajax/cambodiafloodededucenter/$', views.getCambodiaFloodedEduCenter),
    url(r'^ajax/laosfloodededucenter/$', views.getLaosFloodedEduCenter),
    url(r'^ajax/myanmarfloodededucenter/$', views.getMyanmarFloodedEduCenter),
    url(r'^ajax/thailandfloodededucenter/$', views.getThailandFloodedEduCenter),
    url(r'^ajax/vietnamfloodededucenter/$', views.getVietnamFloodedEduCenter),
]