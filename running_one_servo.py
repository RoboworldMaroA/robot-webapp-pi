#This program will  servo
#This version is better I am using PWM and stop PWM if I do not want to jumping a servo

import cv2

import time

#Dont use AngualServo because servo is unstable
#from gpiozero import AngularServo
#servo =AngularServo(12, initial_angle=-5, min_pulse_width=0.0005, max_pulse_width=0.0027)

#thres = 0.45 # Threshold to detect object
import RPi.GPIO as GPIO

outputForServo1 = 12 #servo up and down

GPIO.setmode(GPIO.BCM)

GPIO.setup(outputForServo1,GPIO.OUT)

angleServo1 = GPIO.PWM(outputForServo1,50)

angleServo1.start(6.5)
time.sleep(3)

angleServo1.ChangeDutyCycle(4)
time.sleep(0.5)
angleServo1.ChangeDutyCycle(0)
time.sleep(3)

angleServo1.ChangeDutyCycle(6)
time.sleep(0.5)
angleServo1.ChangeDutyCycle(0)
time.sleep(3)

# clean
angleServo1.stop()
GPIO.cleanup()