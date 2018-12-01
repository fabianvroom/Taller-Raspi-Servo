# Ejemplo 1. Mover un Servomotor conectado al puerto 12

import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
import time                #Importamos time para poder usar time.sleep
import math		   #Importamos un paquete de matemáticas

import logging
logging.basicConfig(level=logging.DEBUG, filename="/home/pi/Documents/Taller.20180620/logfile", filemode="a+",format="NOMBRE - %(message)s")
logging.info("hello")

#######################
servo=12
######################

GPIO.setmode(GPIO.BOARD)      #Ponemos la Raspberry en modo BOARD (esto solo influye en cómo se llaman los pines)
GPIO.setup(servo,GPIO.OUT)    #Ponemos el pin del servo como salida
p = GPIO.PWM(servo,50)        #Ponemos el pin del servo en modo PWM y enviamos 50 pulsos por segundo

# la posición inicial y final del servomotor esta definida por los siguientes valores
# si se pone fuera de ese rango, el servo cruje
inicial=3.5			
final=11

# Se arranca el servo
p.start(inicial)

# En este bloque se define el comportamiento del servomotor
#################################################################

# En esta lista se puede poner cualquier valor
posiciones=[1,-1]
# Aquí se define el tiempo en segundos que tardará el programa en recorrer la lista
ciclo=2

#posiciones=[i for i in range(100)]
#posiciones=[i for i in range(100)]+[100-i for i in range(100)]
#posiciones=[math.cos(i/100*2*math.pi) for i in range(100)]
#################################################################

# estas lineas son para asegurarme de que no os salís del rango (NO TOCAL)
maximo=max(posiciones)
minimo=min(posiciones)
posiciones=[(float(i)-minimo)/(maximo-minimo)*(final-inicial)+inicial for i in posiciones]

# Aquí está la acción del programa
try:                 
	while True:      #iniciamos un loop infinito	
		for i in posiciones:
			p.ChangeDutyCycle(i)
			time.sleep(ciclo/len(posiciones))
			
			# Para indicar en el log lo que estamos haciendo
			s = "SERVO "+str(servo)+" posición: "+ str(math.floor(i*10)/10) 
			logging.info(s)

except KeyboardInterrupt:             # Si el usuario pulsa CONTROL+C entonces...
        p.stop()                      # Detenemos el servo         
        GPIO.cleanup()                # Limpiamos los pines GPIO de la Raspberry y cerramos el script
