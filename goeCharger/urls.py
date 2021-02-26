from django.urls import path
from . import views

urlpatterns = [
    path('', views.goe_index, name='goeCharger_index'),
]
