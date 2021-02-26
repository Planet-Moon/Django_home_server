from django.shortcuts import render
import requests

def goe_index(request):
    return render(request, 'goe_index.html', {})
