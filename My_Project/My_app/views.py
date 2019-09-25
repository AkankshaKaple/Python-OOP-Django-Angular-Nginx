from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def static_page(request):
    return HttpResponse("My Static Page!!")


def dynamic_page(request):
    return render(request, 'home.html', {'name': 'Akanksha'})
