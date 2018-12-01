# EJEMPLO 5. Respuesta simple del servomotor ante un estimulo

import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
import time                #Importamos time para poder usar time.sleep
import math
import random
import logging
logging.basicConfig(level=logging.DEBUG, filename="/home/pi/Documents/Taller.20180620/logfile", filemode="a+",format="NOMBRE - %(message)s")
logging.info("hello")

############################
servo = 8
###########################

GPIO.setmode(GPIO.BOARD)   #Ponemos la Raspberry en modo BOARD
GPIO.setwarnings(False)
# trig (cable amarillo en el prototipo)
GPIO.setup(16, GPIO.IN)
# echo (cable verde en el prototipo)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(servo,GPIO.OUT)    #Ponemos el pin del servo como salida
p = GPIO.PWM(servo,50)        #Ponemos el pin del servo en modo PWM y enviamos 50 pulsos por segundo
t=0               
inicial=3.5
final=11
p.start(inicial)
try:                 
	while True:      #iniciamos un loop infinito
		start = 0
		end = 0
		#print('1')
		# Configura el sensor
		GPIO.output(18, False)
		#time.sleep(2) # 2 segundos para hacer el programa usable
		#print('2')
		# Empezamos a medir
		GPIO.output(18, True)
		time.sleep(0.00001) #10 microsegundos
		GPIO.output(18, False)

		# Flanco de 0 a 1 = inicio 
		while GPIO.input(16) == GPIO.LOW:
		    start = time.time()
		#print('3')
		# Flanco de 1 a 0 = fin
		while GPIO.input(16) == GPIO.HIGH:
		    end = time.time()
		#print('4')
		# el tiempo que devuelve time() estÃ¡ en segundos
		distancia = (end-start) * 343 / 2
		#print ("Distancia al objeto =", str(distancia))	
#####################################################################################################

		if distancia < 0.15:
			posiciones=[inicial]
		else:
			posiciones=[final]
		ciclo=0.2
#####################################################################################################

		# estas lineas son para asegurarme de que no os salís del rango (NO TOCAR)
		maximo=max(posiciones)
		minimo=min(posiciones)
		if maximo != minimo:
			posiciones=[(float(i)-minimo)/(maximo-minimo)*(final-inicial)+inicial for i in posiciones]
				
			
		for i in posiciones:
			p.ChangeDutyCycle(i)
			time.sleep(ciclo/len(posiciones))

			 # Para indicar en el log lo que estamos haciendo
			s = "SERVO "+str(servo)+" posición: "+ str(math.floor(i*10)/10)
			logging.info(s)

except KeyboardInterrupt:             # Si el usuario pulsa CONTROL+C entonces...
	p.stop()                      # Detenemos el servo
	GPIO.cleanup()                # Limpiamos los pines GPIO de la Raspberry y cerramos el script




