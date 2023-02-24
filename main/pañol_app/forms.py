
from dataclasses import field
from pickle import TRUE

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

NOMBREEQUIPOS= [
    ('Decodificador Cisco', 'Decodificador Cisco'),
    ('Decodificador_Sagemcom_DCIW303', 'Decodificador_Sagemcom_DCIW303'),
    ('Decodificador_Digital_4K_BASICO_DCIW362', 'Decodificador_Digital_4K_BASICO_DCIW362'),
    ('Decodificador_Digital_4K_387', 'Decodificador_Digital_4K_387'),
    ('Video_Sound_Box_Sagemcom_393','Video_Sound_Box_Sagemcom_393'),
    ('Modem_2_0','Modem_2_0'),
    ('Modem_3_0','Modem_3_0'),
    ('Modem_3_1','Modem_3_1'),
    ]

class CargarEquiposAStock(forms.Form):
    seriado=forms.CharField(widget=forms.Textarea)

class IngresoDeEquipos(forms.Form):
    nombre_equipo=forms.CharField(label='Selecionar EQUIPO', widget=forms.Select(choices=NOMBREEQUIPOS))
    seriado=forms.CharField(widget=forms.Textarea)

class Bobina_consumoform(forms.Form):
    consumo=forms.CharField(widget=forms.NumberInput)
    

    
class Bobina_hisotiralform(forms.Form):
    seriado_bobina=forms.CharField(widget=forms.TextInput)

class IngresoDeEquiposNoOperativos(forms.Form):
    seriado=forms.CharField(widget=forms.Textarea)