from django.urls import path
from . import views, api
from django.conf.urls import include, url
#from oauth2client.contrib.django_util.site import urls as oauth2_urls

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('mbee/', views.MapBoxView.as_view(), name='mbee'),
    path('lee/', views.LeafletView.as_view(), name='lee'),
    path('olmap/', views.olGeoserver.as_view(), name='olmap'),
    path('olee/', views.olView.as_view(), name='olee'),

    path('map/', views.MapView.as_view(), name='mapviewer'),
    path('usecase/', views.UsecaseView.as_view(), name='usecase'),
    path('usecase/01/', views.Usecase01.as_view(), name='usecase01'),
    path('usecase/02/', views.Usecase02.as_view(), name='usecase02'),
    path('usecase/03/', views.Usecase03.as_view(), name='usecase03'),
    #path('about/', views.AboutView.as_view(), name='about'),
    path('about/', views.TeamList.as_view(), name='about'),
    path('people/<slug:slug>/', views.TeamDetailView.as_view(), name='team-detail'),
    #url(r'^ajax/date/$', api.dateList),
    url(r'^ajax/precipmap/$', api.get_precipitation_map),
    url(r'^ajax/potentialfloodmap/$', api.get_potential_flood_map),
    url(r'^ajax/surfacewatermap/$', api.get_dailysurface_water_map),
    url(r'^ajax/permanaentwatermap/$', api.get_permanent_water_map),
    url(r'^ajax/doymap/$', api.get_doy_map),

    url(r'^ajax/floodagemap/$', api.get_flood_age_map),
    url(r'^ajax/flooddurationmap/$', api.get_flood_duration_map),

    url(r'^ajax/downloadfloodmap/$', api.get_download_url),
    url(r'^ajax/casefloodmap/$', api.get_case_flood_map),
    url(r'^ajax/jrcpermanentwatermap/$', api.get_jrc_permanent_water_map),
    url(r'^ajax/cambodiafloodedarea/$', views.getCambodiaFloodedArea),
    url(r'^ajax/laosfloodedarea/$', views.getLaosFloodedArea),
    url(r'^ajax/myanmarfloodedarea/$', views.getMyanmarFloodedArea),
    url(r'^ajax/thailandfloodedarea/$', views.getThailandFloodedArea),
    url(r'^ajax/vietnamfloodedarea/$', views.getVietnamFloodedArea),

    url(r'^ajax/cambodiafloodeddistricts/$', views.getCambodiaFloodedDistricts),
    url(r'^ajax/laosfloodeddistricts/$', views.getLaosFloodedDistricts),
    url(r'^ajax/myanmarfloodeddistricts/$', views.getMyanmarFloodedDistricts),
    url(r'^ajax/thailandfloodeddistricts/$', views.getThailandFloodedDistricts),
    url(r'^ajax/vietnamfloodeddistricts/$', views.getVietnamFloodedDistricts),

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
    
    url(r'^ajax/elmap/$', api.get_eel_map),
     url(r'^ajax/depthmap/$', api.get_flood_depth_map),
]