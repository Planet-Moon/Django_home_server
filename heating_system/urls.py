from django.urls import path
from . import views

urlpatterns = [
    path('', views.heating_index, name='heating_index'),
]