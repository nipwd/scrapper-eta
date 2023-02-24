import datetime
import time  # type: ignore
from datetime import timedelta
from time import sleep
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
#chrome_options.add_argument("--start-maximized")
#driver = webdriver.Chrome('./chromedriver')
driver = webdriver.Chrome(chrome_options=chrome_options)
###
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
#chrome_options.add_argument('headless')
#chrome_options.add_argument("--start-maximized")

#driver = webdriver.Chrome('./chromedriver')
page= 'https://docs.google.com/spreadsheets/'
chrome_driver_binary = 'driver/chrome.exe'
actionChains = ActionChains(driver)
today = datetime.date.today()
today = (today.strftime('%d-%m-%Y'))
bot = telebot.TeleBot(':')

mac =''


### code
driver.get(page)
title = driver.title
final_url = driver.current_url
print("Empezando el scrap en: ",title)
print(final_url)
driver.implicitly_wait(10)
#datos = driver.find_element(By.XPATH, "/html/body/div[5]/div/div[4]/table/tbody/tr[2]/td[4]/div/div[2]/div/div/div")
datos = driver.find_element(By.XPATH, "/html/body/div[5]/div/div[4]/table/tbody/tr[2]/td[2]/div/div[2]/div/div/div")

print(datos.text)

datos = actionChains.move_to_element(datos).perform()
actionChains.click(datos).perform()

datos2 = driver.find_element(By.XPATH, "/html/body/div[5]/div/div[4]/table/tbody/tr[2]/td[3]/div/div[3]/div/div[66]")
datos = actionChains.move_to_element(datos2).perform()
actionChains.click(datos2).perform()
print(datos2.text)
#buscar_equipos = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[4]/div[1]/div[1]/div[2]")))
#actionChains.click(buscar_equipos).perform()
datos2.send_keys(Keys.CONTROL, 'f')
sleep(3)
datos_buscar = driver.find_element(By.XPATH, '//*[@id="docs-findbar-input"]/table/tbody/tr/td[1]/input')
actionChains.move_to_element(datos_buscar).perform()
actionChains.click(datos_buscar).perform()
datos_buscar.send_keys(f"{mac}")
datos_buscar.send_keys(Keys.ESCAPE, Keys.ARROW_RIGHT, "hecho", Keys.ENTER)
sleep(5)
print("end")
driver.close()
driver.quit()