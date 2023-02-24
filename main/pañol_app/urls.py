from django.urls import path

from pañol_app.views import *

urlpatterns = [
    path('',index, name='index'),
    path('tecnicos/',tecnicos, name='tecnicos'),
    path('devolcuiones/',devolcuiones, name='devolcuiones'),
    path('Ingresos/',Ingresos, name='Ingresos'),
    path('verTecnico/<tecnico_name>', verTecnico, name="verTecnico"),  # type: ignore
    path('descuentos/', descuentos, name="descuentos"),
]
