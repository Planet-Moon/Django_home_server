from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from goeCharger_django.models import GoeCharger as GoeCharger_model
from goeCharger_django.models import Car
from goeCharger import GOE_Charger as goeCharger
from goeCharger_django.forms import CarForm, TestForm


def goe_charger_index(request):
    chargers = GoeCharger_model.objects.all().order_by("-created_on")
    cars = Car.objects.all()


    context = {"chargers": chargers, "cars": cars}
    return render(request, "goe_charger_index.html", context)



def goe_charger_category(request, category):
    chargers = GoeCharger_model.objects.filter(categories__name__contains=category).order_by(
        "-created_on"
    )
    context = {"category": category, "chargers": chargers}
    return render(request, "goe_charger_category.html", context)



def goe_charger_detail(request,title):
    goe_charger = GoeCharger_model.objects.get(title=title)
    car = Car.objects.get(pk=goe_charger.connected_car.pk)


    initial_form = {"charger": goe_charger.title}
    car_form = CarForm(initial=initial_form)
    if request.method == 'POST':
        car_form = CarForm(request.POST)
        if car_form.is_valid():
            data = car_form.cleaned_data
            goe_charger.connected_car = data["change_car"]
            goe_charger.save()

    test_form = TestForm()

    charger_data = {}

    if True:
        try:
            charger = goeCharger("http://"+goe_charger.ipAddress)


            if int(charger.car) > 1:
                car = "connected"
            else:
                car = "not connected"
            charger_data["car"] = car
            charger_data["amp"] = charger.amp
            if charger.alw:
                alw = "charging"
            else:
                alw = "not charging"
            charger_data["alw"] = alw
            charger_data["nrg"] = charger.data.get("nrg")[11]*10
            if charger.power_threshold < 0:
                pwr_thresh = "not configured"
                pwr_thresh_unit = ""
            else:
                pwr_thresh = str(charger.power_threshold)
                pwr_thresh_unit = "A"
            charger_data["min_amp"] = pwr_thresh
            charger_data["min_amp_unit"] = pwr_thresh_unit
            charger_data["connection"] = True
            charger_data["error"] = None
        except Exception as e:
            charger_data["connection"] = False
            charger_data["error"] = str(e)
    else:
        charger_data["connection"] = True
        charger_data["error"] = None
        charger_data["car"] = "Connected"
        charger_data["amp"] = 8
        charger_data["alw"] = "not charging"
        charger_data["nrg"] = 0
        charger_data["min_amp"] = "not configured"
        charger_data["min_amp_unit"] = ""

    context = {"charger":goe_charger, "charger_data":charger_data, "car_form":car_form, "test_form":test_form}
    return render(request, 'goe_charger_detail.html', context)
