from django.shortcuts import render
from goeCharger import GOE_Charger as goeCharger

def goe_index(request):
    goe_charger = goeCharger("http://192.168.178.106")
    context = {}
    if int(goe_charger.car) > 1:
        car = "connected"
    else:
        car = "not connected"
    context["car"] = car
    context["amp"] = goe_charger.amp
    if goe_charger.alw:
        alw = "charging"
    else:
        alw = "not charging"
    context["alw"] = alw

    if goe_charger.power_threshold < 0:
        pwr_thresh = "not configured"
        pwr_thresh_unit = ""
    else:
        pwr_thresh = str(goe_charger.power_threshold)
        pwr_thresh_unit = "A"
    context["min_amp"] = pwr_thresh
    context["min_amp_unit"] = pwr_thresh_unit
    return render(request, 'goe_index.html', context)
