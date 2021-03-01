from django.urls import path
from . import views

urlpatterns = [
    path('', views.goe_charger_index, name='goe_charger_index'),
    path('charger/<title>/', views.goe_charger_detail, name='goe_charger_detail'),
    path('category/<category>/', views.goe_charger_category, name='goe_charger_category'),
]
