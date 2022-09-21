from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mapclient.urls')),
    path('loaderio-33986448e3ce0d95a570f5c4e1a73b45.txt', TemplateView.as_view(template_name='loaderio-33986448e3ce0d95a570f5c4e1a73b45.txt', content_type='text/plain')),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)