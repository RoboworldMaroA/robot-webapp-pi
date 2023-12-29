#Program the measure distance using ultrasonic sensor HC-SR04
#Program is used in Raspberry Pi 4 4 wheeled mobile robot
#Wirtual environment tflite-env 
#Marek Augustyn
#29 Dec 2023
#Import Libraries

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG = 20
ECHO = 21

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, True)
time.sleep(0.0001)
GPIO.output(TRIG, False)

while GPIO.input(ECHO) == False:
      start = time.time()
      
while GPIO.input(ECHO) == True:
    end = time.time()

sig_time = end-start
      
distance = sig_time / 0.000058

print ('Distance: {} cm'.format(distance))

GPIO.cleanup()
