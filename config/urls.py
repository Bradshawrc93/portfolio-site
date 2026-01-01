"""Portfolio Site URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('', include('core.urls')),
    path('devlog/', include('devlog.urls')),
    path(f'{settings.ADMIN_PATH}', admin.site.urls),
]

admin.site.site_header = "Portfolio Site Admin"
admin.site.site_title = "Portfolio Site Admin"
admin.site.index_title = "Administration"

