# EJEMPLO 3: USO DE HEBRAS PARA CONTROLAR 2 MOTORES A LA VEZ
# coding=utf-8
import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
import time                #Importamos time para poder usar time.sleep
import math
import random
import threading
import logging
logging.basicConfig(level=logging.DEBUG, filename="/home/pi/Documents/Taller.20180620/logfile", filemode="a+",format="NOMBRE - %(message)s")
logging.info("hello")

################
servos=[8,10] # esta vez los servos están definidos en una lista
################

GPIO.setmode(GPIO.BOARD)   	#Ponemos la Raspberry en modo BOARD
p = []				
GPIO.setup(servos[0],GPIO.OUT)    	#Ponemos el primer servo como salida
p.append( GPIO.PWM(8,50) )      	#Ponemos el primer servo en modo PWM y enviamos 50 pulsos por segundo
GPIO.setup(servos[1],GPIO.OUT)    	#Ponemos el segundo servo como salida
p.append( GPIO.PWM(10,50) )     	#Ponemos el segundo en modo PWM y enviamos 50 pulsos por segundo

# Definimos los puntos inicial y final del servo y los arrancamos
inicial=3.5
final=11
p[0].start(inicial)
p[1].start(inicial)

# En esta parte se define el movimiento de los servos
#################################################################
posiciones1=[1,-1]
posiciones2=[1,-1]
ciclo1=2
ciclo2=1.9

#posiciones1=[i for i in range(100)]
#posiciones=[i for i in range(100)]+[100-i for i in range(100)]
#posiciones2=[math.cos(i/100*2*math.pi) for i in range(100)]
#################################################################

# Esta parte es para asegurarnos de que no nos salimos de los límites
maximo=max(posiciones1)
minimo=min(posiciones1)
posiciones1=[(float(i)-minimo)/(maximo-minimo)*(final-inicial)+inicial for i in posiciones1]

maximo=max(posiciones2)
minimo=min(posiciones2)
posiciones2=[(float(i)-minimo)/(maximo-minimo)*(final-inicial)+inicial for i in posiciones2]

# Se define el comportamiento de cada uno de los servos con un método, que luego llamaremos mediante una hebra
def motor(numero,posiciones,ciclo):
	try:
		while True:
			for i in posiciones:
				p[numero].ChangeDutyCycle(i)
				time.sleep(ciclo/len(posiciones))
				s = "SERVO "+str(servos[numero])+" posición: "+ str(math.floor(i*10)/10)
				logging.info(s)

	except KeyboardInterrupt:         #Si el usuario pulsa CONTROL+C entonces...
		p[numero].stop()          #Detenemos el servo
		GPIO.cleanup()            #Limpiamos los pines GPIO de la Raspberry y cerramos el script



t1 = threading.Thread(target=motor,args=(0,posiciones1,ciclo1,))
t2 = threading.Thread(target=motor,args=(1,posiciones2,ciclo2,))

threads=[]
threads.append(t1)
t1.start()

threads.append(t2)
t2.start()

