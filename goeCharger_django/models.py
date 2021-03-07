from django.db import models

class Car_Category(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=20)

class Car(models.Model):
    def __str__(self):
        return self.title
    title = models.CharField(max_length=30)
    battery_capacity = models.IntegerField()
    power_max = models.IntegerField()
    power_min = models.IntegerField()
    soc = models.FloatField(max_length=3) # in %
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Car_Category', related_name='cars')

class Charger_Category(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=20)

class GoeCharger(models.Model):
    def __str__(self):
        return self.title
    title = models.CharField(max_length=30)
    ipAddress = models.GenericIPAddressField()
    power_max = models.IntegerField()
    power_min = models.IntegerField()
    car_selected = models.ForeignKey(Car, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    thread_running = models.BooleanField(default=False)
    categories = models.ManyToManyField('Charger_Category', related_name='goe_chargers')
