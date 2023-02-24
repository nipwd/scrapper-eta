import time  # type: ignore
from datetime import timedelta
from time import sleep

start_time = time.time()
import csv
import datetime
import sqlite3
from sqlite3 import Error

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import telebot
import chromedriver_autoinstaller


chromedriver_autoinstaller.install() 
driver = webdriver.Chrome()
###
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
#chrome_options.add_argument('headless')
chrome_options.add_argument("--start-maximized")
#driver = webdriver.Chrome('./chromedriver')
driver = webdriver.Chrome(chrome_options=chrome_options)
###
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
#chrome_options.add_argument('headless')
page= "page-name"
chrome_driver_binary = 'driver/chrome.exe'
actionChains = ActionChains(driver)
today = datetime.date.today()
today = (today.strftime('%d-%m-%Y'))
bot = telebot.TeleBot('api:key')


### code
driver.get("page-name")
title = driver.title
final_url = driver.current_url
print("Empezando el scrap en: ",title)
print(final_url)
driver.implicitly_wait(10)
#formulario de inicio de sesion
text_box = driver.find_element(by=By.ID, value="username")
submit_button = driver.find_element(by=By.ID, value="sign-in")
text_box.send_keys("username")
form_textfield = driver.find_element(By.NAME, 'password')
form_textfield.send_keys("secret-pass")
submit_button.click()
#seleccionar vista de lista
datos = driver.find_element(By.XPATH, "//*/span[contains(text(),'Vista de lista')]")
datos = actionChains.move_to_element(datos).perform()
actionChains.double_click(datos).perform()
sleep(2)
### empezando el bucle en la lista de tecnicos
with open("lista_tecnicos.csv") as listatecnicos:
    reader = csv.reader(listatecnicos)
    amr_csv = [line[0] for line in reader]
    for tecnico_nombre in amr_csv:
        print("Buscando ordenes de: ",tecnico_nombre)
        buscar_tecnicos = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[14]/div[1]/main/div/div[2]/div[3]/div[1]/div[2]/div/div[2]/div[2]/div/div[1]/table/tr/td[2]/div/table/tr/td[2]/input")))
        buscar_tecnicos.send_keys(Keys.CONTROL, 'a')
        buscar_tecnicos.send_keys(Keys.BACKSPACE)
        buscar_tecnicos.send_keys(f"{tecnico_nombre}" + "\n")
        boton_ruta = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, f'//*/span[contains(text(),"{tecnico_nombre}")]')))
        boton_ruta.click()  ### apreta en el nombre del tecnico y muestra ruta
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.TAG_NAME,'tr')))
        if not driver.find_elements(By.XPATH, ("//*/td[contains(text(),'Reparación')or (contains(text(),'Cambio de Domicilio'))]") ):       # si no ecnuentra ordenes de reparacion seguir
            print(tecnico_nombre, "No Trabajo")
            pass
        if driver.find_elements(By.XPATH, "//*/div[contains(text(),'No hay actividades con fecha de referencia')]"):  # no trabajo
            print(tecnico_nombre, "No Trabajo")
            pass
        else:
            total =len(driver.find_elements(By.XPATH, ("//*/td[contains(text(),'Reparación')or (contains(text(),'Cambio de Domicilio'))]"))) #selecionar la orden y entrar al sub-menu
            print(total)
            count = 0
            while count != total:  #cuenta el total de ordenes a recorrer y no sale del loop hasta terminar
                try:
                    ordenes = driver.find_elements(By.XPATH, ("//*/td[contains(text(),'Reparación')or (contains(text(),'Cambio de Domicilio'))]"))
                    vt = ordenes[count]
                    WebDriverWait(driver, 60).until(EC.visibility_of(vt))
                    vt.click()

                    numero_vt = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[1]/div[1]/div/div[2]/div[10]/div[1]/div/div[2]')))
                    numero_vt= numero_vt.text
                    print(numero_vt)
                    numero_cliente = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[1]/div[1]/div/div[2]/div[14]/div[1]/div/div[2]')))
                    numero_cliente = numero_cliente.text
                    print(numero_cliente)
                    nombre_cliente = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[1]/div[1]/div/div[2]/div[15]/div[1]/div/div[2]')))
                    nombre_cliente=  nombre_cliente.text
                    print(nombre_cliente)
                    try:
                        if driver.find_elements(By.XPATH,"/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[1]/div[1]/div/div[2]/div[16]/div[1]/div/div[2]"):
                            dni_cliente = driver.find_element(By.XPATH, "/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[1]/div[1]/div/div[2]/div[16]/div[1]/div/div[2]")
                            dni_cliente = dni_cliente.text
                        else:
                            dni_cliente= "sin dni"
                    except:
                        continue
                    print(dni_cliente)
                    direccion_cliente = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[3]/div/div[2]/div[1]/div[1]/div/div[2]')))
                    direccion_cliente = direccion_cliente.text
                    print(direccion_cliente)
                    try:
                        if driver.find_elements(By.XPATH,'/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[3]/div/div[2]/div[4]/div[1]/div/div[2]'):
                            localidad_cliente = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[3]/div/div[2]/div[4]/div[1]/div/div[2]')))
                            localidad_cliente = localidad_cliente.text
                        else:
                            localidad_cliente = "Cambio de Domicilio" 
                    except:
                        continue
                    print(localidad_cliente)
                    partido_cliente =   WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[3]/div/div[2]/div[6]/div[1]/div/div[2]')))
                    partido_cliente = partido_cliente.text
                    print(partido_cliente)
                    if driver.find_elements(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[3]/div/div[2]/div[7]/div[1]/div/div[2]'):
                        telefono_cliente = driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[3]/div/div[2]/div[7]/div[1]/div/div[2]')
                        telefono_cliente = telefono_cliente.text
                    else:
                        telefono_cliente = "sin telefono"
                    print(telefono_cliente)
                    try:
                        if driver.find_element(By.XPATH,'/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/div[2]').text == '1':
                            region_cliente = driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[3]/div/div[2]/div[15]/div[1]/div/div[2]')
                            region_cliente = region_cliente.text
                            print(region_cliente)
                        if driver.find_element(By.XPATH,'/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/div[2]').text == '2':
                            region_cliente = driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[3]/div/div[2]/div[14]/div[1]/div/div[2]')
                            region_cliente = region_cliente.text
                            print(region_cliente)
                        if driver.find_element(By.XPATH,'/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/div[2]').text == '3':
                            region_cliente = driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/form/div/div[6]/div[2]/div/div/div/div/div/div[2]/div[3]/div/div[2]/div[14]/div[1]/div/div[2]')
                            region_cliente = region_cliente.text
                            print(region_cliente)
                        
                    except:
                        region_cliente = 'ZONA GENERICA'
                        
                    #######################################################################################
                    if driver.find_elements(By.XPATH, "//*/span[contains(text(),'Inventario')]"):   #si encuentra inventario entrar
                        datos_inv = driver.find_elements(By.XPATH, "//*/span[contains(text(),'Inventario')]")
                        lista = []
                        for e in datos_inv:
                            e.click()
                            try:
                                if not ((driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/div/div/div/div/div[1]/table/thead[2]/tr[1]/td/div/div[2]')).text == "Instalado") and not ((driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/div/div/div/div/div[1]/table/thead[4]/tr[1]/td/div/div[2]')).text == "Instalado"):
                                    print(f"Orden {numero_vt} sin Equipos, no hay instalados")
                                    lista.append(today)
                                    lista.append(tecnico_nombre)
                                    lista.append("Sin Instalado")
                                    lista.append("Sin Instalado")
                                    lista.append("Sin Retiro")
                                    lista.append("Sin Retiro")
                                    lista.append(numero_vt)
                                    lista.append(numero_cliente)
                                    lista.append(nombre_cliente)
                                    lista.append(dni_cliente)
                                    lista.append(direccion_cliente)
                                    lista.append(localidad_cliente)
                                    lista.append(partido_cliente)
                                    lista.append(telefono_cliente)
                                    lista.append(region_cliente)
                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                    print(df)
                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                    lista.pop()
                                if (driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/div/div/div/div/div[1]/table/thead[2]/tr[1]/td/div/div[2]')).text == "Instalado":
                                    if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[1]/tr[1]'):
                                        lista = []
                                        datos_ = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[1]/tr[1]') # 1 instalado
                                        for e in datos_:
                                            data = e.text.split("\n")
                                            lista.append(today)
                                            lista.append(tecnico_nombre)
                                            lista.append(data[0])
                                            lista.append(data[1])
                                    if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[1]'):  # 1 desinstalado
                                        desinstalados = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[1]')
                                        for x in desinstalados:
                                            desinsta_ = x.text.split("\n")
                                            lista.append(desinsta_[0])
                                            lista.append(desinsta_[1])
                                            lista.append(numero_vt)
                                            lista.append(numero_cliente)
                                            lista.append(nombre_cliente)
                                            lista.append(dni_cliente)
                                            lista.append(direccion_cliente)
                                            lista.append(localidad_cliente)
                                            lista.append(partido_cliente)
                                            lista.append(telefono_cliente)
                                            lista.append(region_cliente)
                                            df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                            print(df)
                                            df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                            lista.pop()
                                            continue
                                    if not driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[1]'): # si no hay 1 desinstalado
                                            lista.append("Sin Retiro")
                                            lista.append("Sin Retiro")
                                            lista.append(numero_vt)
                                            lista.append(numero_cliente)
                                            lista.append(nombre_cliente)
                                            lista.append(dni_cliente)
                                            lista.append(direccion_cliente)
                                            lista.append(localidad_cliente)
                                            lista.append(partido_cliente)
                                            lista.append(telefono_cliente)
                                            lista.append(region_cliente)
                                            df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                            print(df)
                                            df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                            lista.pop()
                                            continue
                                    if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[1]/tr[2]'): # 2 instalados
                                            lista= []
                                            datos_2 = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[1]/tr[2]')
                                            for e2 in datos_2:
                                                data2 = e2.text.split("\n")
                                                lista.append(today)
                                                lista.append(tecnico_nombre)
                                                lista.append(data2[0])
                                                lista.append(data2[1])
                                            if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[2]'): # 2 desinstalados
                                                desinstalados = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[2]')
                                                for x2 in desinstalados:
                                                    desinsta_2 = x2.text.split("\n")
                                                    lista.append(desinsta_2[0])
                                                    lista.append(desinsta_2[1])
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    continue
                                            if not driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[2]'): #  si no hay 2 desinstalado
                                                    lista.append("Sin Retiro")
                                                    lista.append("Sin Retiro")
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    continue
                                    if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[1]/tr[3]'): # 3 instalados
                                            lista= []
                                            datos_3 = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[1]/tr[3]')
                                            for e3 in datos_3:
                                                data3 = e3.text.split("\n")
                                                lista.append(today)
                                                lista.append(tecnico_nombre)
                                                lista.append(data3[0])
                                                lista.append(data3[1])
                                            if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[3]'): # 3 desinstalados
                                                desinstalados = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[3]')
                                                for x3 in desinstalados:
                                                    desinsta_3 = x3.text.split("\n")
                                                    lista.append(desinsta_3[0])
                                                    lista.append(desinsta_3[1])
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    continue
                                            if not driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[3]'): #  si no hay 3 desinstalado
                                                    lista.append("Sin Retiro")
                                                    lista.append("Sin Retiro")
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    continue  
                                    if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[1]/tr[4]'): # 4 instalados
                                            lista= []
                                            datos_4 = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[1]/tr[4]')
                                            for e4 in datos_4:
                                                data4 = e4.text.split("\n")
                                                lista.append(today)
                                                lista.append(tecnico_nombre)
                                                lista.append(data4[0])
                                                lista.append(data4[1])
                                            if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[4]'): # 4 desinstalados
                                                desinstalados = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[4]')
                                                for x4 in desinstalados:
                                                    desinsta_4 = x4.text.split("\n")
                                                    lista.append(desinsta_4[0])
                                                    lista.append(desinsta_4[1])
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    continue
                                            if not driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[4]'): #  si no hay 4 desinstalado
                                                    lista.append("Sin Retiro")
                                                    lista.append("Sin Retiro")
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    continue 
                                    if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[1]/tr[5]'): # 5 instalados
                                            lista= []
                                            datos_5 = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[1]/tr[5]')
                                            for e5 in datos_5:
                                                data5 = e5.text.split("\n")
                                                lista.append(today)
                                                lista.append(tecnico_nombre)
                                                lista.append(data5[0])
                                                lista.append(data5[1])
                                            if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[5]'): # 5 desinstalados
                                                desinstalados = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[5]')
                                                for x5 in desinstalados:
                                                    desinsta_5 = x5.text.split("\n")
                                                    lista.append(desinsta_5[0])
                                                    lista.append(desinsta_5[1])
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    continue
                                            if not driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[5]'): #  si no hay 5 desinstalado
                                                    lista.append("Sin Retiro")
                                                    lista.append("Sin Retiro")
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    continue 
                                    if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[1]/tr[6]'): # 6 instalados
                                            lista= []
                                            datos_6 = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[1]/tr[6]')
                                            for e6 in datos_6:
                                                data6 = e6.text.split("\n")
                                                lista.append(today)
                                                lista.append(tecnico_nombre)
                                                lista.append(data6[0])
                                                lista.append(data6[1])
                                            if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[6]'): # 6 desinstalados
                                                desinstalados = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[6]')
                                                for x6 in desinstalados:
                                                    desinsta_6 = x6.text.split("\n")
                                                    lista.append(desinsta_6[0])
                                                    lista.append(desinsta_6[1])
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    continue
                                            if not driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[6]'): #  si no hay 6 desinstalado
                                                    lista.append("Sin Retiro")
                                                    lista.append("Sin Retiro")
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    continue 
                                    
                                
                                if (driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/div/div/div/div/div[1]/table/thead[4]/tr[1]/td/div/div[2]')).text == "Instalado":
                                    if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[1]'): # 1 instalados
                                        datos_2 = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[1]')
                                        for e2 in datos_2:
                                            data2 = e2.text.split("\n")
                                            lista.append(today)
                                            lista.append(tecnico_nombre)
                                            lista.append(data2[0])
                                            lista.append(data2[1])
                                            if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[1]'):  # 1 desinstalado
                                                if (driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/div/div/div/div/div[1]/table/thead[6]/tr/td/div/div[2]')).text == "Desinstalado":
                                                    desinstalados = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[1]')
                                                    for x in desinstalados:
                                                        desinsta_ = x.text.split("\n")
                                                        lista.append(desinsta_[0])
                                                        lista.append(desinsta_[1])
                                                        lista.append(numero_vt)
                                                        lista.append(numero_cliente)
                                                        lista.append(nombre_cliente)
                                                        lista.append(dni_cliente)
                                                        lista.append(direccion_cliente)
                                                        lista.append(localidad_cliente)
                                                        lista.append(partido_cliente)
                                                        lista.append(telefono_cliente)
                                                        lista.append(region_cliente)
                                                        df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                        print(df)
                                                        df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                        lista.pop()
                                                        break
                                                if (driver.find_element(By.XPATH, '/html/body/div[14]/div[1]/main/div/div[2]/div[2]/div/div[2]/div/div/div/div/div[1]/table/thead[6]/tr/td/div/div[2]')).text == "Recurso":
                                                    lista.append("Sin Retiro")
                                                    lista.append("Sin Retiro")
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    break

                                            if not driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[1]'): # si no hay 1 desinstalado
                                                lista.append("Sin Retiro")
                                                lista.append("Sin Retiro")
                                                lista.append(numero_vt)
                                                lista.append(numero_cliente)
                                                lista.append(nombre_cliente)
                                                lista.append(dni_cliente)
                                                lista.append(direccion_cliente)
                                                lista.append(localidad_cliente)
                                                lista.append(partido_cliente)
                                                lista.append(telefono_cliente)
                                                lista.append(region_cliente)
                                                df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                print(df)
                                                df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                lista.pop()
                                                break
                                    if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[2]'): # 2 instalados
                                            datos_2 = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[2]')
                                            lista= []
                                            for e2 in datos_2:
                                                data2 = e2.text.split("\n")
                                                lista.append(today)
                                                lista.append(tecnico_nombre)
                                                lista.append(data2[0])
                                                lista.append(data2[1])
                                            if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[2]'): # 2 desinstalados
                                                desinstalados = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[2]')
                                                for x2 in desinstalados:
                                                    desinsta_2 = x2.text.split("\n")
                                                    lista.append(desinsta_2[0])
                                                    lista.append(desinsta_2[1])
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    break
                                            if not driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[2]'): #  si no hay 2 desinstalado
                                                    lista.append("Sin Retiro")
                                                    lista.append("Sin Retiro")
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    break
                                    if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[3]'): # 3 instalados
                                            lista= []
                                            datos_3 = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[3]')
                                            for e3 in datos_3:
                                                data3 = e3.text.split("\n")
                                                lista.append(today)
                                                lista.append(tecnico_nombre)
                                                lista.append(data3[0])
                                                lista.append(data3[1])
                                            if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[3]'): # 3 desinstalados
                                                desinstalados = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[3]')
                                                for x3 in desinstalados:
                                                    desinsta_3 = x3.text.split("\n")
                                                    lista.append(desinsta_3[0])
                                                    lista.append(desinsta_3[1])
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    break
                                            if not driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[3]'): #  si no hay 3 desinstalado
                                                    lista.append("Sin Retiro")
                                                    lista.append("Sin Retiro")
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    break  
                                    if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[4]'): # 4 instalados
                                            lista= []
                                            datos_4 = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[4]')
                                            for e4 in datos_4:
                                                data4 = e4.text.split("\n")
                                                lista.append(today)
                                                lista.append(tecnico_nombre)
                                                lista.append(data4[0])
                                                lista.append(data4[1])
                                            if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[4]'): # 4 desinstalados
                                                desinstalados = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[4]')
                                                for x4 in desinstalados:
                                                    desinsta_4 = x4.text.split("\n")
                                                    lista.append(desinsta_4[0])
                                                    lista.append(desinsta_4[1])
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    break
                                            if not driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[4]'): #  si no hay 4 desinstalado
                                                    lista.append("Sin Retiro")
                                                    lista.append("Sin Retiro")
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    break 
                                    if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[5]'): # 5 instalados
                                            lista= []
                                            datos_5 = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[5]')
                                            for e5 in datos_5:
                                                data5 = e5.text.split("\n")
                                                lista.append(today)
                                                lista.append(tecnico_nombre)
                                                lista.append(data5[0])
                                                lista.append(data5[1])
                                            if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[5]'): # 5 desinstalados
                                                desinstalados = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[5]')
                                                for x5 in desinstalados:
                                                    desinsta_5 = x5.text.split("\n")
                                                    lista.append(desinsta_5[0])
                                                    lista.append(desinsta_5[1])
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    break
                                            if not driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[5]'): #  si no hay 5 desinstalado
                                                    lista.append("Sin Retiro")
                                                    lista.append("Sin Retiro")
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    break 
                                    if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[6]'): # 6 instalados
                                            lista= []
                                            datos_6 = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[2]/tr[6]')
                                            for e6 in datos_6:
                                                data6 = e6.text.split("\n")
                                                lista.append(today)
                                                lista.append(tecnico_nombre)
                                                lista.append(data6[0])
                                                lista.append(data6[1])
                                            if driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[6]'): # 6 desinstalados
                                                desinstalados = driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[6]')
                                                for x6 in desinstalados:
                                                    desinsta_6 = x6.text.split("\n")
                                                    lista.append(desinsta_6[0])
                                                    lista.append(desinsta_6[1])
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                                                    break
                                            if not driver.find_elements(By.XPATH, '//*[@id="content"]/div/div/div/div/div[1]/table/tbody[3]/tr[6]'): #  si no hay 6 desinstalado
                                                    lista.append("Sin Retiro")
                                                    lista.append("Sin Retiro")
                                                    lista.append(numero_vt)
                                                    lista.append(numero_cliente)
                                                    lista.append(nombre_cliente)
                                                    lista.append(dni_cliente)
                                                    lista.append(direccion_cliente)
                                                    lista.append(localidad_cliente)
                                                    lista.append(partido_cliente)
                                                    lista.append(telefono_cliente)
                                                    lista.append(region_cliente)
                                                    df = pd.DataFrame([lista], columns=['fecha','tecnico','equipo_instalado','mac_instalado','equipo_desinstalado','mac_desinstalado','numero_vt','numero_cliente','nombre_cliente','dni_cliente','direccion_cliente','localidad_cliente','partido_cliente','telefono_cliente','region_cliente'])
                                                    print(df)
                                                    df.to_csv('csv/hechos.csv', mode='a', header=False, index=False)
                                                    lista.pop()
                            except :
                              continue
                    count = count + 1
                    boton_atras = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,"//*/span[contains(text(),'Detalles de actividad')]"))) #vuelve a la lisa de ordenes 
                    boton_atras.click()
                    boton_atras2 = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,"//*/span[contains(text(),'Consola de despacho')]")))#vuelve a la lisa de ordenes
                    boton_atras2.click()
                except Exception:
                    continue

conn = sqlite3.connect('db.sqlite3'.format('pañol_app_equiposretirados'))
df = pd.read_csv('csv/hechos.csv')
df.to_sql('pañol_app_equiposretirados', conn, index=True, index_label='id',  if_exists='replace')
print(df)
#bot.send_message(chat_id='id-chat', text="Scrap completado con Exito") ----CHAT PRIVADO
conn.close()
#WebDriverWait(driver, 240).until(EC.visibility_of_element_located((By.XPATH,"//*/div[contains(text(),'NS')]"))): #apreta el boton NS para cerrar sesion y desconectarse
#cerrar = WebDriverWait(driver, 240).until(EC.visibility_of_element_located((By.XPATH,"//*/div[contains(text(),'NS')]"))) #apreta el boton NS para cerrar sesion y desconectarse
#cerrar_boton = actionChains.move_to_element(cerrar).perform()
#actionChains.click(cerrar_boton).perform()
#cerrar_sesión = WebDriverWait(driver, 240).until(EC.element_to_be_clickable((By.XPATH, "//*/span[contains(text(),'Cerrar sesión')]")))
#cerrar_sesión = actionChains.move_to_element(cerrar_sesión).perform()
#actionChains.click(cerrar_sesión).perform()
#sleep(2)
sec =(time.time() - start_time)
td = timedelta(seconds=sec)
print('Tiempo de Ejecucion', td)  # Time in hh:mm:ss:
driver.close()
driver.quit()
bot.send_message(chat_id='-', text="Programa finalizado, Tiempo de Ejecucion: {}".format(td))

total = df[(df["fecha"]==today)].count() # total de ordenes  en el dia




bot.send_message(chat_id='-id', text="total de ordenes en el dia: {}".format(total[0]))







