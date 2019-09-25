from django.urls import path, include
from . import views


urlpatterns = [

    path('', views.dynamic_page, name='dynamic_page'),
    path('', views.static_page, name='static_page')
]