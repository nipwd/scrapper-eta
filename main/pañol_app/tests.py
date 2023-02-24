from django.test import TestCase

# Create your tests here.
import datetime
from datetime import timedelta
today = datetime.date.today()
ayer = today - timedelta(days = 1)
ayer = (ayer.strftime('%d-%m-%Y'))
print(ayer)


from models import EquiposRetirados, Equipo
def descuento():
    field_name = 'mac_desinstalado'
    obj = EquiposRetirados.objects.first()
    field_value = getattr(obj, field_name)
    print(field_value)
    for e in field_value:
        if Equipo.objects.filter(seriado= e):
            print("esta")
        if not Equipo.objects.filter(seriado= e):
            print("no esta")



retiro = EquiposRetirados.objects.get().mac_desinstalado
ingreso=Equipo.objects.get().seriado
if retiro not in ingreso:
    data = EquiposRetirados.objects.filter(mac_desinstalado=retiro)
    print(data)