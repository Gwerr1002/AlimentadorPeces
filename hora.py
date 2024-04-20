import network, time, sys
import ntptime

def conectaWifi(red, password):
     global miRed
     miRed = network.WLAN(network.STA_IF)     
     if not miRed.isconnected():              #Si no está conectado…
         miRed.active(True)                   #activa la interface
         miRed.connect(red, password)         #Intenta conectar con la red
         print('Conectando a la red', red +"…")
         timeout = time.time()
         while not miRed.isconnected():           #Mientras no se conecte..
             if (time.ticks_diff (time.time(), timeout) > 10):
                 return False
     return True

i2c = I2C(1,scl=Pin(22), sda=Pin(21))
lcd = SSD1306_I2C (64,48,i2c)

ntptime.host = "cronos.cenam.mx"
timezone = -6 #UTC-6
lcd.fill (0)
lcd.text ("Wifi…",0,0,1)
lcd.show ()

if conectaWifi ("LeonardoDePisa", "Ua666GoYLb!"):
    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    #Indicar conexion exitosa
    lcd.fill (0)
    lcd.text ("Wifi OK",0,0,1) 
    lcd.show () 
    time.sleep (1) 
    lcd.fill (0) 
    try:
        #Sincroniza fecha y hora     
        ntptime.settime ()
    except:
        #Error     
        print ("Error NTP!")
        lcd.fill (0)
        lcd.text ("NTP ERR",0,0,1)
        lcd.text ("RESET",0,10,1)
        lcd.show ()
        sys.exit () 
    #Desconecta el Wifi para ahorrar energía
    miRed.active (False) 
    while (True):
       #Muestra hora y fecha en el display     
       hora_local_seg = time.time () + timezone * 3600  #Hora local en segundos     
       hora_local = time.localtime (hora_local_seg)     #Pasa a tupla de 8 elementos     
       #Imprimir hora_local en LCD
       lcd.fill (0)     #Imprime la hora     
       lcd.text ("{:02}".format (hora_local[3]),10,10,1)     
       lcd.text (":", 25,10,2)     
       lcd.text ("{:02}".format (hora_local[4]),32,10,1)     
       #Imprime la fecha     
       lcd.text ("{:02}".format (hora_local[2]),10,20,1)     
       lcd.text ("/", 25,20,2)     
       lcd.text ("{:02}".format (hora_local[1]),32,20,1)     
       lcd.show()
else:
     print ("Imposible conectar")
     lcd.fill (0) 
     lcd.text ("Wifi ERR",0,0,1) 
     lcd.text ("RESET",0,10,1) 
     lcd.show () 
     sys.exit ()
