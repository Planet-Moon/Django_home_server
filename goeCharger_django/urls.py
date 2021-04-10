from django.urls import path
from . import views

urlpatterns = [
    path('', views.goe_charger_index, name='goe_charger_index'),
    path('cars', views.cars_index, name='cars_index'),
    path('car/<title>', views.car_detail, name='car_detail'),
    path('carcategory/<category>/', views.car_category, name='car_category'),
    path('charger/<title>/', views.goe_charger_detail, name='goe_charger_detail'),
    path('chargercategory/<category>/', views.goe_charger_category, name='goe_charger_category'),
    path('chargerlog/<charger_title>/', views.goe_charger_log, name='goe_charger_log'),
    path('chargerlog/<charger_title>/<variable>', views.goe_charger_log_variable, name='goe_charger_log_variable'),
]
