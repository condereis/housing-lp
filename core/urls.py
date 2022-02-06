from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/estimate_request/', views.estimate_request, name='estimate_request'),
]
