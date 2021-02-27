from django.shortcuts import render
from goeCharger import GOE_Charger as goeCharger

def goe_index(request):
    goe_charger = goeCharger("http://192.168.178.106")
    context = {}
    context["car"] = goe_charger.car
    context["amp"] = goe_charger.amp
    context["alw"] = str(goe_charger.alw)
    return render(request, 'goe_index.html', context)
