from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.utils import timezone
from goeCharger_django.models import GoeCharger as GoeCharger_model
from goeCharger_django.models import Car
from goeCharger import GOE_Charger as goeCharger
from goeCharger_django.models import GoeChargerDailyLog
from goeCharger_django.forms import CarForm, PublishForm


import logging
import threading
import time
import sys
import datetime

logger = logging.getLogger(__name__)

if "runserver" in sys.argv:
    import paho.mqtt.client as mqtt

    goe_charger_instances = dict()

    class Server_MQttClient(object):
        def __init__(self):
            self.server_topic = "home_test_server"
            self.client = mqtt.Client()
            self.client.on_connect = self.onMQTTConnect
            self.client.on_message = self.onMQTTMessage
            self.client.on_publish = self.onMQTTPublish
            self.client.connect_async("192.168.178.107")
            self.client.loop_start()

        def onMQTTMessage(self, client, userdata, msg):
            topic = msg.topic
            topics = topic.split("/")
            payload = msg.payload.decode("utf-8")
            # logger.info(topic + ": " + payload)
            if len(topics) < 4:
                return
            if topics[0] == "$SYS":
                logger.debug(topic + ": "+payload)
            elif topics[3] == "command":
                if topics[4] == "car_selected":
                    charger = GoeCharger_model.objects.get(title=topics[2])
                    try:
                        change_car = Car.objects.get(title=payload)
                    except:
                        return
                    charger.car_selected = change_car
                    with database_semaphore:
                        charger.save()
                    self.client.publish("/".join(topics[:-1])+"/min-amp",charger.car_selected.power_min,qos=0,retain=False) # set min amp to new selected car
                    self.client.publish("/".join(topics[:-2])+"/status/car_selected",charger.car_selected.title,qos=0,retain=True) # set status to new selected car

                    # set amp to min-amp of new selected car if amp is lower
                    if int(goe_charger_instances[charger.title].amp) < charger.car_selected.power_min:
                        self.client.publish("/".join(topics[:-1])+"/amp",charger.car_selected.power_min,qos=0,retain=False)
            elif topics[3] == "status":
                if GoeChargerDailyLog.objects.count():
                    delete_records = GoeChargerDailyLog.objects.exclude(time__range=[timezone.now() - datetime.timedelta(minutes=1), timezone.now()])
                    delete_records.delete()
                new_log_record = GoeChargerDailyLog()
                new_log_record.goeCharger = GoeCharger_model.objects.get(title=topics[2])
                new_log_record.variable = topics[4]
                new_log_record.value = payload
                new_log_record.save()


        def onMQTTConnect(self, client, userdata, flags, rc):
            logger.info(str(client)+" server mqtt connected with result code "+str(rc))
            self.client.subscribe(self.server_topic+"/#")
            self.client.subscribe("$SYS/broker/clients/connected")
            self.client.subscribe("$SYS/broker/messages/inflight")
            self.client.subscribe("$SYS/broker/load/connections/+")

        def onMQTTPublish(self, client, userdata, mid):
            pass
    server_mqtt = Server_MQttClient()


    def reset_running():
        chargers = GoeCharger_model.objects.all()
        for charger in chargers:
            charger.thread_running = False
            charger.save()
    reset_running()

    database_semaphore = threading.Semaphore()

    class GoeCharger_thread(threading.Thread):
        def __init__(self, goeCharger):
            self.goeCharger = goeCharger
            threading.Thread.__init__(self, name=goeCharger.name+"_thread")

        def run(self):
            charger = GoeCharger_model.objects.get(title=self.goeCharger.name)
            logging.info("charger: "+str(charger))
            if charger:
                logging.info("running: "+str(charger.thread_running))
                if not charger.thread_running:
                    charger.thread_running = True
                    charger.save()
                    self.goeCharger.start_loop()

    def create_goe_instances():
        chargers = GoeCharger_model.objects.all()
        _goe_charger_instances = dict()
        for charger in chargers:
            goe_charger_instance = goeCharger(
                name=charger.title,
                address="http://"+charger.ipAddress,
                mqtt_topic="home_test_server/goe_charger/"+charger.title,
                mqtt_broker="192.168.178.107",
                mqtt_port=1883)
            _goe_charger_instances[charger.title] = goe_charger_instance
            GoeCharger_thread(goe_charger_instance).start()
            charger_topic = "home_test_server/goe_charger/"+charger.title
            server_mqtt.client.publish(charger_topic+"/status/car_selected",payload=charger.car_selected.title,qos=0,retain=True)
            server_mqtt.client.publish(charger_topic+"/command/min-amp",payload=charger.car_selected.power_min,qos=0,retain=False)
            time.sleep(1)
        return _goe_charger_instances
    goe_charger_instances = create_goe_instances()
    logger.info(goe_charger_instances)


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


def cars_index(request):
    cars = Car.objects.all()
    return render(request, "cars_index.html", context={"cars": cars})


def car_detail(request,title):
    car = Car.objects.get(title=title)
    connected_chargers = GoeCharger_model.objects.filter(car_selected=car)
    return render(request, "car_detail.html", context={"car": car, "connected_chargers": connected_chargers})

def car_category(request,category):
    cars = Car.objects.filter(categories__name__contains=category).order_by(
        "-created_on"
    )
    context = {"category": category, "cars": cars}
    return render(request, "cars_category.html", context)


def goe_charger_detail(request,title):
    goe_charger = GoeCharger_model.objects.get(title=title)
    car = Car.objects.get(pk=goe_charger.car_selected.pk)


    initial_form = {"change_car": car.pk}
    car_form = CarForm(initial=initial_form)
    if request.method == 'POST':
        car_form = CarForm(request.POST)
        if car_form.is_valid():
            data = car_form.cleaned_data
            goe_charger.car_selected = data["change_car"]
            goe_charger.save()

    publish_form = PublishForm()

    context = {"charger":goe_charger, "car_form":car_form, "publish_form":publish_form}
    return render(request, 'goe_charger_detail.html', context)

def goe_charger_log(request,charger_title):
    goe_charger = GoeCharger_model.objects.get(title=charger_title)
    data = list(GoeChargerDailyLog.objects.filter(goeCharger=goe_charger).values())
    result_data = dict()
    for i in range(len(data)):
        del data[i]["goeCharger_id"]
        del data[i]["id"]
        try:
            result_data[data[i]["variable"]].append({"value":[data[i]["value"]],"time":data[i]["time"]})
        except:
            result_data[data[i]["variable"]] = [{"value":data[i]["value"],"time":data[i]["time"]}]
    return JsonResponse(result_data, safe=False)

def goe_charger_log_variable(request,charger_title,variable):
    goe_charger = GoeCharger_model.objects.get(title=charger_title)
    data = list(GoeChargerDailyLog.objects.filter(goeCharger=goe_charger).filter(variable=variable).values())
    result = []
    for i in range(len(data)):
        result.append({"value": data[i]["value"], "time": data[i]["time"].strftime("%Y-%m-%dT%H:%M:%S")})
    del data
    return JsonResponse(result, safe=False)
