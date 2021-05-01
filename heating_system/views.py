from django.shortcuts import render

def heating_index(request):
    context = {"context_item":"context_item"}
    return render(request, 'heating_index.html', context)
