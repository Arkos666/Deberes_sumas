from django.contrib import admin
from django.urls import path, include
from .views import index, crear_pdf, visitas

urlpatterns = [
    path('', index, name='index'),
    path('crear_pdf/', crear_pdf, name='crear_pdf'),
    path('visitas/', visitas, name='visitas'),

]


