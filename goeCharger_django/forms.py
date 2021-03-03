from django import forms
from django.db.models.functions import Lower
from goeCharger_django.models import Car, GoeCharger

def get_free_cars():
    cars = Car.objects.order_by(Lower('title').asc())
    chargers = GoeCharger.objects.all()
    taken_cars = []
    for i in chargers:
        taken_cars.append(i.connected_car)
    free_cars = [x for x in cars if x not in taken_cars]
    return free_cars

class CarForm(forms.Form):
    change_car = forms.ModelChoiceField(queryset=Car.objects.all().order_by(Lower('title').asc())) # case insensitive, alphabetic order
    charger = forms.CharField(widget=forms.HiddenInput())
    # def __init__(self, charger=None, *args, **kwargs):
    #     super(CarForm, self).__init__(*args, **kwargs)
    #     self.fields["charger"] = forms.CharField(widget=forms.TextInput(), empty_value="charger.title")
    pass

class TestForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={
                'id': 'test-text',
                'required': True,
                'placeholder': 'Publish something...'}))

# To make values default do this in views.py:
#
# initial_form = {"charger": goe_charger.title}
#     car_form = CarForm(initial=initial_form)


