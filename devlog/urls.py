from django.urls import path
from . import views

urlpatterns = [
    path('', views.devlog_list, name='devlog_list'),
    path('<slug:slug>/', views.devlog_detail, name='devlog_detail'),
]

