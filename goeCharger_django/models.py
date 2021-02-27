from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=20)

class GoeCharger(models.Model):
    title = models.CharField(max_length=30)
    ipAddress = models.CharField(max_length=15)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name='posts')
