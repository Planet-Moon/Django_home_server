from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from goeCharger_django.models import GoeCharger as GoeCharger_model
from goeCharger_django.models import Car
from goeCharger import GOE_Charger as goeCharger
from goeCharger_django.forms import CarForm, PublishForm


import logging
import threading
import time

logger = logging.getLogger(__name__)

import paho.mqtt.client as mqtt
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
        logger.info(topic + ": " + payload)
        if len(topics) < 4:
            return
        if topics[3] == "command":
            if topics[4] == "change_car":
                charger = GoeCharger_model.objects.get(title=topics[2])
                try:
                    change_car = Car.objects.get(title=payload)
                except:
                    return
                charger.car_selected = change_car
                charger.save()
                self.client.publish("/".join(topics[:-1])+"/min-amp",charger.car_selected.power_min,qos=0,retain=False)
                self.client.publish("/".join(topics[:-2])+"/status/car_selected",charger.car_selected.title,qos=0,retain=True)
            pass
        else:
            pass

    def onMQTTConnect(self, client, userdata, flags, rc):
        logger.info(str(client)+"Connected with result code "+str(rc))
        self.client.subscribe(self.server_topic+"/#")
        self.client.subscribe("$SYS/broker/clients/connected")

    def onMQTTPublish(self, client, userdata, mid):
        pass
server_mqtt = Server_MQttClient()


def reset_running():
    chargers = GoeCharger_model.objects.all()
    for charger in chargers:
        charger.thread_running = False
        charger.save()
reset_running()

class GoeCharger_thread(threading.Thread):
    def __init__(self, goeCharger):
        self.goeCharger = goeCharger
        threading.Thread.__init__(self)

    def run(self):
        # self.goeCharger.stop_loop()
        ipAddress = self.goeCharger.address.replace("http://","")
        charger = GoeCharger_model.objects.get(title=self.goeCharger.name)
        logging.info("charger: "+str(charger))
        if charger:
            logging.info("running: "+str(charger.thread_running))
            if not charger.thread_running:
                charger.thread_running = True
                charger.save()
                self.goeCharger.start_loop()

goe_chargers_instances = []
def create_goe_instances():
    chargers = GoeCharger_model.objects.all()
    for charger in chargers:
        goe_charger_instance = goeCharger(
            name=charger.title,
            address="http://"+charger.ipAddress,
            mqtt_topic="home_test_server/goe_charger/"+charger.title,
            mqtt_broker="192.168.178.107",
            mqtt_port=1883)
        goe_chargers_instances.append(goe_charger_instance)
        GoeCharger_thread(goe_charger_instance).start()
        charger_topic = "home_test_server/goe_charger/"+charger.title
        server_mqtt.client.publish(charger_topic+"/status/car_selected",payload=charger.car_selected.title,qos=0,retain=True)
        server_mqtt.client.publish(charger_topic+"/command/min-amp",payload=charger.car_selected.power_min,qos=0,retain=False)
        time.sleep(1)
create_goe_instances()


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
