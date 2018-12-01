
#EJEMPLO 4: LECTURA DEL SENSOR DE ULTRASONIDOS

import time
import RPi.GPIO as GPIO
import logging
logging.basicConfig(level=logging.DEBUG, filename="/home/pi/Documents/Taller.20180620/logfile", filemode="a+",format="NOMBRE - %(message)s")
logging.info("hello")

# Configurar el GPIO con convenio de numerado Board
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# trig (cable amarillo en el prototipo)
GPIO.setup(16, GPIO.IN)
# echo (cable verde en el prototipo)
GPIO.setup(18, GPIO.OUT)

try:
    while True:
        time.sleep(2) #para que haya tiempo entre medidas y no os choqueis los unos con los otros
        
        #se pone el trigger a 0
        GPIO.output(18, False)
        time.sleep(2) # 2 segundos para hacer el programa usable
        # Empezamos a medir
        GPIO.output(18, True)
        time.sleep(0.00001) #10 microsegundos
        GPIO.output(18, False)

        # Flanco de 0 a 1 = inicio 
        while GPIO.input(16) == GPIO.LOW:
            start = time.time()
 
       # Flanco de 1 a 0 = fin
        while GPIO.input(16) == GPIO.HIGH:
            end = time.time()
 
        # el tiempo que devuelve time() está en segundos
        distancia = (end-start) * 343 / 2
        print ("Distancia al objeto =", str(distancia))
        
except KeyboardInterrupt:
    print("\nFin del programa")
    GPIO.output(18, False)
    GPIO.cleanup()
