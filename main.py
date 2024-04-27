import network, time, sys
import ntptime
from machine import I2C, reset
from ssd1306 import SSD1306_I2C
from motor import Pin, Motor28BYJ

#Hora de alimentación
refH = "20:57:00 Hrs"

#Configuración WiFi
nameNet="NombreRedWifi"
password="Contraseña"
#Configuración del tiempo
ntptime.host = "cronos.cenam.mx"
timezone = -6 #UTC-6
#Configuración motor
motor = Motor28BYJ()
#Configuración OLED
i2c = I2C(1,scl=Pin(22), sda=Pin(21))
lcd = SSD1306_I2C (128,64,i2c)
lcd.fill(0)
lcd.text("Conectando Wifi ...",0,0,1)
lcd.show()

def conectaWifi(red, password):
     global miRed,lcd
     miRed = network.WLAN(network.STA_IF)     
     if not miRed.isconnected():              #Si no está conectado…
         miRed.active(True)                   #activa la interface
         miRed.connect(red, password)         #Intenta conectar con la red
         print(f'Conectando a la red {red} ...')
         timeout = time.time()
         while not miRed.isconnected():           #Mientras no se conecte..
             if (time.ticks_diff(time.time(), timeout) > 10):
                 return False
     return True

def sincronizaFechaHora():
    global lcd
    try:
        #Sincroniza fecha y hora     
        ntptime.settime()
    except:
        #Error     
        print ("Error del host!")
        lcd.fill(0)
        lcd.text("Network error",0,0,1)
        lcd.text("RESET...",0,10,1)
        time.sleep(1)
        lcd.show()
        reset()

def alimentar():
    global lcd,motor
    lcd.fill(0)
    lcd.show()
    lcd.text("Alimentando",10,30)
    lcd.text("peces cx",10,40)
    lcd.show()
    motor.step(1, 4100, 0.001)
    motor.clean()

if conectaWifi(nameNet, password):
    print("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    #Indicar conexion exitosa
    lcd.fill(0)
    lcd.text("Wifi OK",0,0,1) 
    lcd.show() 
    time.sleep(1) 
    lcd.fill(0) 
    sincronizaFechaHora()
    #Desconecta el Wifi para ahorrar energía
    miRed.active(False) 
    while True:
       #Muestra hora y fecha en el display     
       hora_local_seg = time.time() + timezone * 3600  #Hora local en segundos     
       hora_local = time.localtime(hora_local_seg)     #Pasa a tupla de 8 elementos     
       #Imprimir hora_local en LCD
       lcd.fill(0)     #Imprime la hora
       hrs = f"{hora_local[3]:02}:{hora_local[4]:02}:{hora_local[5]:02} Hrs"
       lcd.text(hrs,10,10,1)  
       #Imprime la fecha
       fech = f"{hora_local[2]:02}/{hora_local[1]:02}/{hora_local[0]:02}"
       lcd.text(fech,10,30,1)
       lcd.show()
       if hrs == refH:
           alimentar()
       elif hrs == '23:59:00 Hrs':
           reset()
else:
     print("Imposible conectar")
     lcd.fill(0)
     lcd.text("Wifi ERROR",0,0,1) 
     lcd.text("RESET",0,10,1) 
     lcd.show()
     reset()
