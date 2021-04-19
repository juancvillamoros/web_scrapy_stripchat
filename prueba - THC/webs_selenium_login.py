#system libraries

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import random
import urllib
import os
import sys
import time

import pandas as pd

opc = Options()
opc.add_argument("user-agent=Mozilla/5.0 (X11; Linux x85_64) AppleWebKit/537.36(KHTML, like Gecko)")

driver = webdriver.Chrome('./chromedriver/chromedriver.exe', options=opc)
driver.get('https://es.stripchat.com/login')

user = "fnietzshe"
password = open('password.txt').readline().strip()

#Aquí está el código para resolver el user y password

input_user = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/main/div[2]/div[3]/div/div/div/div[2]/form/div[1]/input'))
)


input_user = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/main/div[2]/div[3]/div/div/div/div[2]/form/div[1]/input')
input_pass = driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div/main/div[2]/div[3]/div/div/div/div[2]/form/div[2]/input')

input_user.send_keys(user)
input_pass.send_keys(password)

#Aquí está el código para resolver el Recaptcha


audioToTextDelay = 10
delayTime = 2
audioFile = "\\payload.mp3"
URL = "https://www.google.com/recaptcha/api2/demo"
SpeechToTextURL = "https://speech-to-text-demo.ng.bluemix.net/"

def delay():
    time.sleep(random.randint(2, 3))

def audioToText(audioFile):
    driver.execute_script('''window.open("","_blank")''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(SpeechToTextURL)

    delay()
    audioInput = driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[2]/button')
    audioInput.send_keys(audioFile)

    time.sleep(audioToTextDelay)

    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')
    while text is None:
        text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')

    result = text.text

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return result


try:
    # create chrome driver
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-notifications')
    # option.add_argument('--mute-audio')
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    driver = webdriver.Chrome(os.getcwd() + "\\chromedriver.exe", options=option)
    delay()
    # go to website which have recaptcha protection
    driver.get(URL)
except Exception as e:
    sys.exit(
        "[-] Please update the chromedriver.exe in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")

g_recaptcha = driver.find_element(By.XPATH, 'id#recaptcha-anchor-label')[0]
outerIframe = g_recaptcha.find_element_by_tag_name('/html/body/div/div')
outerIframe.click()

iframes = driver.find_elements_by_id('#rc-imageselect > div.rc-imageselect-payload')
audioBtnFound = False
audioBtnIndex = -1

for index in range(len(iframes)):
    driver.switch_to.default_content()
    iframe = driver.find_elements_by_id('#rc-imageselect > div.rc-imageselect-payload')[index]
    driver.switch_to.frame(iframe)
    driver.implicitly_wait(delayTime)
    try:
        audioBtn = driver.find_element_by_id("recaptcha-anchor > div.recaptcha-checkbox-border")
        audioBtn.click()
        audioBtnFound = True
        audioBtnIndex = index
        break
    except Exception as e:
        pass

if audioBtnFound:
    try:
        while True:
            # get the mp3 audio file
            src = driver.find_element_by_id("audio-source").get_attribute("src")
            print("[INFO] Audio src: %s" % src)

            # download the mp3 audio file from the source
            urllib.request.urlretrieve(src, os.getcwd() + audioFile)

            # Speech To Text Conversion
            key = audioToText(os.getcwd() + audioFile)
            print("[INFO] Recaptcha Key: %s" % key)

            driver.switch_to.default_content()
            iframe = driver.find_elements_by_tag_name('iframe')[audioBtnIndex]
            driver.switch_to.frame(iframe)

            # key in results and submit
            inputField = driver.find_element_by_id("audio-response")
            inputField.send_keys(key)
            delay()
            inputField.send_keys(Keys.ENTER)
            delay()

            err = driver.find_elements_by_class_name('rc-audiochallenge-error-message')[0]
            if err.text == "" or err.value_of_css_property('display') == 'none':
                print("[INFO] Success!")
                break

    except Exception as e:
        print(e)
        sys.exit("[INFO] Possibly blocked by google. Change IP,Use Proxy method for requests")
else:
    sys.exit("[INFO] Audio Play Button not found! In Very rare cases!")


#Aquí está el código para dar clic en el botón de inicio de sesión
button = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/main/div[2]/div[3]/div/div/div/div[2]/form/div[4]/button')
button.click()

#Aquí está el código para acceder a la modelo

opcs = Options()
opcs.add_argument("user-agent=Mozilla/5.0 (X11; Linux x85_64) AppleWebKit/537.36(KHTML, like Gecko)")

driver = webdriver.Chrome('./chromedriver/chromedriver.exe', optiones=opcs)
driver.get('https://es.stripchat.com/')

modelo = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/main/div[2]/div[3]/div/div/div/div[2]/form/div[1]/input'))
)

#Entra al transmision de la modelo
modelo = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/main/div[2]/div[3]/div/div[2]/div/div/div[3]/div[2]/div[1]/div/section/div[1]/a')
modelo.click()

#Entra a la sección de perfil de la modelo
perfil = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/main/div[2]/div[3]/div/div/div/div[1]/div/nav[1]/div[1]/div[2]/a')
perfil.click()

#Datos del perfil de la modelo
datos = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/main/div[2]/div[3]/div/div/div/div[3]/div/div/div[4]/div/div[1]/div[1]/div/div/div')
datos = datos.text
datos_perfil = datos.split('Perfil')[0].split('\n')[1:-1]

nombre = list()
de = list()
idiomas = list()
edad = list()
cuerpo = list()
detalles = list()
etnia = list()
pelo = list()
ojos = list()
subcultura= list()
redes = list()

for i in range(0, len(datos_perfil), 12):
    nombre.append(datos_perfil[i])
    de.append(datos_perfil[i+1])
    idiomas.append(datos_perfil[i+2])
    edad.append(datos_perfil[i+3])
    cuerpo.append(datos_perfil[i+5])
    detalles.append(datos_perfil[i+6])
    etnia.append(datos_perfil[i+7])
    pelo.append(datos_perfil[i+8])
    ojos.append(datos_perfil[i+9])
    subcultura.append(datos_perfil[i+10])
    redes.append(datos_perfil[i+11])

df = pd.DataFrame({'Nombre': nombre, 'Nacionalidad': de, 'Idiomas': idiomas, 'Edad': edad, 'Cuerpo': cuerpo,'Detalles': detalles,'Etnia': etnia,'Pelo': pelo,'C_Ojos': ojos, 'Subcultura': subcultura,'R_Sociales': redes })
print(df)
df.to_csv('datos_modelo.csv', index=False)
driver.quit()


