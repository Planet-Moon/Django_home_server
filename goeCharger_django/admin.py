from django.contrib import admin
from goeCharger_django.models import Car_Category, Car, Charger_Category, GoeCharger

class Car_CategoryAdmin(admin.ModelAdmin):
    pass

class CarAdmin(admin.ModelAdmin):
    pass
class Charger_CategoryAdmin(admin.ModelAdmin):
    pass

class GoeChargerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Car_Category, Car_CategoryAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Charger_Category, Charger_CategoryAdmin)
admin.site.register(GoeCharger, GoeChargerAdmin)
