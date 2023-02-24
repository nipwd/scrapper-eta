import csv
from datetime import datetime, timedelta
from urllib import request

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import DatabaseError, IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, Template
from django.db.models import Sum
from decimal import Decimal

from pañol_app.forms import *
from pañol_app.models import *

today = datetime.today()
ayer = today - timedelta(days = 1)
ayer = (ayer.strftime('%d-%m-%Y'))
antesayer = today - timedelta(days = 2)
antesayer = (antesayer.strftime('%d-%m-%Y'))

def index(request):
    with open("/mnt/c/Users/main/Desktop/telecentro/lista_tecnicos.csv") as listatecnicos:
        reader = csv.reader(listatecnicos)
        amr_csv = [line[0] for line in reader]
        for tecnico_nombre in amr_csv:
            name = tecnico_nombre
            instalado = EquiposRetirados.objects.filter(tecnico=name)
            for x in instalado:
                e= x.mac_instalado
                if Equipo.objects.filter(seriado=e).exists():
                    Equipo.objects.filter(seriado=e).update(estado='Instalado')
                    print(e, 'INSTALADO')
                else:
                    continue
        return render(request,'templates/index.html')

def tecnicos(request): # tecnico
    listatecnicos = Tecnico.objects.all()#.order_by('name')
    context = {"name" : listatecnicos}
    return render(request,'templates/tecnicos.html',context)

def Ingresos(request):
    if (request.method == "POST"):
        form= IngresoDeEquipos(request.POST)
        if form.is_valid():
            form.cleaned_data
            text= request.POST.get('seriado')
            if text:
                for line in text.split('\r\n'):
                    nombre_equipo = request.POST.get('nombre_equipo')
                    estado= "pañol"
                    cargar_equipos= Equipo(seriado=line,nombre_equipo=nombre_equipo,estado=estado)
                    try:
                        cargar_equipos.save()
                        Equipo.objects.filter(seriado='').delete()
                        form= IngresoDeEquipos()
                    except IntegrityError:
                        continue
                return render(request,'templates/Ingresos.html', {'formulario': form})
            if not text:
                form= IngresoDeEquipos()
                return render(request,'templates/Ingresos.html', {'formulario': form})
    else:
        form= IngresoDeEquipos()
        return render(request,'templates/Ingresos.html', {'formulario': form})
    return render(request,'templates/Ingresos.html') 


def verTecnico(request,tecnico_name): # tecnico
    listatecnicos = Tecnico.objects.all()
    tecnico= Tecnico.objects.get(name=tecnico_name)
    descu= Descuento.objects.filter(tecnico=tecnico_name)
    
    cable_bobina = int(Tecnico.objects.get(name=tecnico_name).metros)
    equipos= EquiposRetirados.objects.filter(tecnico=tecnico_name).filter(fecha=ayer).exclude(mac_instalado="Sin Instalado")
    equipos_dcisco= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Decodificador Cisco")
    equipos_dsagem= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Decodificador_Sagemcom_DCIW303")
    equipos_4k362= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Decodificador_Digital_4K_BASICO_DCIW362")
    equipos_4k387= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Decodificador_Digital_4K_387")
    equipos_alexa= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Video_Sound_Box_Sagemcom_393")
    equipos_2_0= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Modem_2_0")
    equipos_3_0= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Modem_3_0")
    equipos_3_1= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Modem_3_1")
    listanueva =[]
    for x in listatecnicos:
        listanueva.append(x.name)
    posicion = listanueva.index(tecnico_name)
    siguiente = posicion + 1
    if siguiente ==  len(listanueva):
        siguiente = listanueva[0]
    else:
        siguiente = listanueva[siguiente]
    anterior = posicion -1
    anterior = listanueva[anterior]
    if request.GET.get('valor_data'):
        valor_data= request.GET.get('valor_data')
        valor_data = datetime.strptime(valor_data, '%Y-%m-%d')
        valor_data = (valor_data.strftime('%d-%m-%Y'))
        listatecnicos = Tecnico.objects.all()
        tecnico= Tecnico.objects.get(name=tecnico_name)
        equipos= EquiposRetirados.objects.filter(tecnico=tecnico_name).filter(fecha=valor_data)
        equipos_dcisco= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Decodificador Cisco")
        equipos_dsagem= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Decodificador_Sagemcom_DCIW303")
        equipos_4k362= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Decodificador_Digital_4K_BASICO_DCIW362")
        equipos_4k387= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Decodificador_Digital_4K_387")
        equipos_alexa= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Video_Sound_Box_Sagemcom_393")
        equipos_2_0= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Modem_2_0")
        equipos_3_0= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Modem_3_0")
        equipos_3_1= Equipo.objects.filter(estado=tecnico_name).filter(nombre_equipo = "Modem_3_1")
        listanueva =[]
        for x in listatecnicos:
           listanueva.append(x.name)
        posicion = listanueva.index(tecnico_name)
        siguiente = posicion + 1
        if siguiente ==  len(listanueva):
            siguiente = listanueva[0]
        else:
            siguiente = listanueva[siguiente]
            anterior = posicion -1
            anterior = listanueva[anterior]
        form= CargarEquiposAStock()
        form2= Bobina_consumoform()
        form3= Bobina_hisotiralform()
        

        return render(request,'templates/test.html', {'descu':descu,'formulario': form,"siguiente":siguiente,"anterior":anterior,"nombre.name":tecnico_name, "name":listatecnicos,"nombre":tecnico.name,"equipos":equipos,"equipos_dcisco":equipos_dcisco,"equipos_dsagem":equipos_dsagem,"equipos_4k362":equipos_4k362,"equipos_4k387":equipos_4k387,"equipos_alexa":equipos_alexa,"equipos_2_0":equipos_2_0,"equipos_3_0":equipos_3_0,"equipos_3_1":equipos_3_1,"cable_bobina":cable_bobina})
   
    if (request.method == "POST"):
        form= CargarEquiposAStock(request.POST, request.FILES)
        form2= Bobina_consumoform()
        form3= Bobina_hisotiralform()
        if form.is_valid():
            form.cleaned_data
            text= request.POST.get('seriado')
            lista = []
            try:
                if text:
                    for line in text.split('\r\n'):
                       print(line)
                       Equipo.objects.filter(seriado=line).update(estado=tecnico_name)
                    form= CargarEquiposAStock()
                    form2= Bobina_consumoform()
                    form3= Bobina_hisotiralform()
                    return render(request,'templates/test.html', {'descu':descu,'form2':form2,'form3':form3,'formulario': form,"siguiente":siguiente,"anterior":anterior,"nombre.name":tecnico_name, "name":listatecnicos,"nombre":tecnico.name,"equipos":equipos,"equipos_dcisco":equipos_dcisco,"equipos_dsagem":equipos_dsagem,"equipos_4k362":equipos_4k362,"equipos_4k387":equipos_4k387,"equipos_alexa":equipos_alexa,"equipos_2_0":equipos_2_0,"equipos_3_0":equipos_3_0,"equipos_3_1":equipos_3_1,"cable_bobina":cable_bobina})
            except:
                form= CargarEquiposAStock(request.POST, request.FILES)
                form2= Bobina_consumoform()
                form3= Bobina_hisotiralform()
                return render(request,'templates/test.html', {'descu':descu,'form2':form2,'form3':form3,'formulario': form,"siguiente":siguiente,"anterior":anterior,"nombre.name":tecnico_name, "name":listatecnicos,"nombre":tecnico.name,"equipos":equipos,"equipos_dcisco":equipos_dcisco,"equipos_dsagem":equipos_dsagem,"equipos_4k362":equipos_4k362,"equipos_4k387":equipos_4k387,"equipos_alexa":equipos_alexa,"equipos_2_0":equipos_2_0,"equipos_3_0":equipos_3_0,"equipos_3_1":equipos_3_1,"cable_bobina":cable_bobina})
    
    if (request.method == "POST"):
        form2= Bobina_consumoform(request.POST, request.FILES)
        form= CargarEquiposAStock()
        form3= Bobina_hisotiralform()
        if form2.is_valid():
            form2.cleaned_data
            text= request.POST.get('consumo')
            consumo = Bobina_consumo(consumo_bobina=text,tecnico=tecnico_name)
            consumo.save()
            agregar = (Tecnico.objects.get(name=tecnico_name)).metros - int(text)
            Tecnico.objects.filter(name=tecnico_name).update(metros= agregar)
            form= CargarEquiposAStock()
            form2= Bobina_consumoform()
            form3= Bobina_hisotiralform()
            print(consumo)
            return render(request,'templates/test.html', {'descu':descu,'formulario':form,'form3':form3,'form2': form2,"siguiente":siguiente,"anterior":anterior,"nombre.name":tecnico_name, "name":listatecnicos,"nombre":tecnico.name,"equipos":equipos,"equipos_dcisco":equipos_dcisco,"equipos_dsagem":equipos_dsagem,"equipos_4k362":equipos_4k362,"equipos_4k387":equipos_4k387,"equipos_alexa":equipos_alexa,"equipos_2_0":equipos_2_0,"equipos_3_0":equipos_3_0,"equipos_3_1":equipos_3_1,"cable_bobina":cable_bobina})
    if (request.method == "POST"):
        form3= Bobina_hisotiralform(request.POST, request.FILES)
        form3= Bobina_hisotiralform(request.POST, request.FILES)
        form= CargarEquiposAStock()
        form2= Bobina_consumoform()
        if form3.is_valid():
            form3.cleaned_data
            text= request.POST.get('seriado_bobina')
            consumo = Bobina_hisotiral(seriado_bobina=text,tecnico=tecnico_name)
            consumo.save()
            agregar = (Tecnico.objects.get(name=tecnico_name)).metros + 305
            Tecnico.objects.filter(name=tecnico_name).update(metros= agregar)
            form= CargarEquiposAStock()
            form2= Bobina_consumoform()
            form3= Bobina_hisotiralform()
            print(consumo)
            return render(request,'templates/test.html', {'descu':descu,'form2':form2,'formulario':form,'form3': form3,"siguiente":siguiente,"anterior":anterior,"nombre.name":tecnico_name, "name":listatecnicos,"nombre":tecnico.name,"equipos":equipos,"equipos_dcisco":equipos_dcisco,"equipos_dsagem":equipos_dsagem,"equipos_4k362":equipos_4k362,"equipos_4k387":equipos_4k387,"equipos_alexa":equipos_alexa,"equipos_2_0":equipos_2_0,"equipos_3_0":equipos_3_0,"equipos_3_1":equipos_3_1,"cable_bobina":cable_bobina})
        
    else:
        form= CargarEquiposAStock()
        form2= Bobina_consumoform()
        form3= Bobina_hisotiralform()
        return render(request,'templates/test.html', {'descu':descu,'formulario':form,'form2':form2,'form3': form3,'form2':form2,'formulario': form,"siguiente":siguiente,"anterior":anterior,"nombre.name":tecnico_name, "name":listatecnicos,"nombre":tecnico.name,"equipos":equipos,"equipos_dcisco":equipos_dcisco,"equipos_dsagem":equipos_dsagem,"equipos_4k362":equipos_4k362,"equipos_4k387":equipos_4k387,"equipos_alexa":equipos_alexa,"equipos_2_0":equipos_2_0,"equipos_3_0":equipos_3_0,"equipos_3_1":equipos_3_1,"cable_bobina":cable_bobina})




def devolcuiones(request):
    if (request.method == "POST"):
        form= IngresoDeEquiposNoOperativos(request.POST)
        if form.is_valid():
            form.cleaned_data
            text= request.POST.get('seriado')
            if text:
                for line in text.split('\r\n'):
                    print(line)
                    if EquiposRetirados.objects.filter(mac_desinstalado=line).exists():
                        nombre_equipo = EquiposRetirados.objects.get(mac_desinstalado=line).equipo_desinstalado
                        estado= 'Invenario_de_devolucion'
                        cargar_equipos= Equipo(seriado=line,nombre_equipo=nombre_equipo,estado=estado)
                        print(cargar_equipos.seriado, cargar_equipos.nombre_equipo, cargar_equipos.estado)
                        cargar_equipos.save()
                        Equipo.objects.filter(seriado='').delete()
                        form= IngresoDeEquiposNoOperativos()
                    if Equipo.objects.filter(seriado=line).exists():
                        estado= 'Invenario_de_devolucion'
                        Equipo.objects.filter(seriado=line).update(estado= estado)

                        Equipo.objects.filter(seriado='').delete()
                        form= IngresoDeEquiposNoOperativos()
                    else:
                        form= IngresoDeEquiposNoOperativos()
                        pass
                   
                return render(request,'templates/devolcuiones.html', {'formulario': form})
            if not text:
                form= IngresoDeEquiposNoOperativos()
                return render(request,'templates/devolcuiones.html', {'formulario': form})
    else:
        form= IngresoDeEquiposNoOperativos()
        return render(request,'templates/devolcuiones.html', {'formulario': form})
    form= IngresoDeEquiposNoOperativos()
    return render(request,'templates/devolcuiones.html')




def descuentos(request):
    descu= []
    with open("lista_tecnicos.csv") as listatecnicos:
        reader = csv.reader(listatecnicos)
        amr_csv = [line[0] for line in reader]
        for tecnico_nombre in amr_csv:
            name = tecnico_nombre
            
            Descuento.objects.values_list('mac', flat=True).distinct()
            retiro = EquiposRetirados.objects.filter(tecnico=name)
            for x in retiro:
                e= x.mac_desinstalado
                if Equipo.objects.filter(seriado=e).exists():
                    if e == 'Sin Retiro':
                        pass
                    else:
                        print('El equipo', x.equipo_desinstalado, 'esta en proceso de devolucion', e)
                else:
                    if e == 'Sin Retiro':
                        pass
                    else:
                        descuento= Descuento(tecnico=x.tecnico,equipo=x.equipo_desinstalado,mac=x.mac_desinstalado,vt=x.numero_vt,cliente=x.numero_cliente,estado='No descontado')
                        try:
                            descuento.save()
                        except IntegrityError:
                            continue          
    return render(request,'templates/descuento.html',{'descu':descu})
    


