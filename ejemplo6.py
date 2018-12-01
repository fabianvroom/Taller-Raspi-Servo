import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
import time                #Importamos time para poder usar time.sleep
import math
import random
import statistics
import logging
logging.basicConfig(level=logging.DEBUG, filename="/home/pi/Documents/Taller.20180620/logfile", filemode="a+",format="NOMBRE - %(message)s")
logging.info("hello")

##################################################
servo=8
#################################################

GPIO.setmode(GPIO.BOARD)   #Ponemos la Raspberry en modo BOARD
GPIO.setwarnings(False)
# trig (cable amarillo en el prototipo)
GPIO.setup(16, GPIO.IN)
# echo (cable verde en el prototipo)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(servo,GPIO.OUT)    #Ponemos el pin 8 como salida
p = GPIO.PWM(8,50)        #Ponemos el pin 8 en modo PWM y enviamos 50 pulsos por segundo
t=0
p.start(3.5)               
inicial=3.5
final=11.5
aux = []
i = 0 
try:                 
	while True:      #iniciamos un loop infinito
		# pausa de un milisegundo para estabilidad
		time.sleep(0.001)
		# se guarda el tiempo actual para la condicion de escape
		start = time.time()
		end = time.time()
		# Salida del sensor a 0
		GPIO.output(18, False)
		# Salida del sensor a 1 durante 10 milisegundos
		GPIO.output(18, True)
		time.sleep(0.00001)
		GPIO.output(18, False)

		# se calcula el tiempo del flanco de subida
		while GPIO.input(16) == GPIO.LOW:
			start = time.time()
			# condicion de escape (50 milisegundos sin recibir el pulso)
			if (start-end)>0.05:
				#print("escape 1")
				break

		# se calcula el tiempo del flanco de bajada
		while GPIO.input(16) == GPIO.HIGH:
			end = time.time()
			if (end-start)>0.05:
				#print("escape 2")
				break
		# imprimir el tiempo en ms
		#print (str(math.floor((end-start)*10000)/10))
		# se calcula la distancia con la velocidad del sonido
		distancia = (end-start) * 343 / 2
		# imprimir la distancia calculada
		#print ("Distancia al objeto =", str(distancia))	

		# estadística para suavizar los datos
		#aux.append(distancia)
		#aux=aux[-20:]
		#distancia = statistics.median(aux)

#####################################################################################################

		posicion=distancia

####################################################################################################
		
		# se lleva la posición al rango del servo
		posicion = inicial + max(0,min(1,float(posicion))) * ( final - inicial )
		# se coloca el motor en la posición deseada
		p.ChangeDutyCycle(posicion)
		s = "SERVO "+str(servo)+" posición: "+ str(math.floor(posicion*10)/10)
		logging.info(s)

# El ultimo que salga que limpie
except KeyboardInterrupt:         #Si el usuario pulsa CONTROL+C entonces...
        p.stop()                      #Detenemos el servo         
        GPIO.cleanup()                #Limpiamos los pines GPIO de la Raspberry y cerramos el script
