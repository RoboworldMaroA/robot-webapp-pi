#This program control servos - moving camra upu and down
#This version is better I am using PWM and stop PWM if I do not want to jumping a servo
# Servo still is unstable
#This program is exported to  main application robot_webapp_and_sonar_v1

import cv2

import time

#Dont use AngualServo because servo is unstable
#from gpiozero import AngularServo
#servo =AngularServo(12, initial_angle=-5, min_pulse_width=0.0005, max_pulse_width=0.0027)

#thres = 0.45 # Threshold to detect object
import RPi.GPIO as GPIO

outputForServoCameraVertically = 12 #servo up and down
outputForServoCameraHorizontally = 16 #servo up and down

GPIO.setmode(GPIO.BCM)

GPIO.setup(outputForServoCameraVertically,GPIO.OUT)
GPIO.setup(outputForServoCameraHorizontally,GPIO.OUT)
angleServo1 = GPIO.PWM(outputForServoCameraVertically,51)
angleServo2 = GPIO.PWM(outputForServoCameraHorizontally,51)

inputAngleServoCameraHorizontally = 6


 #Home position in front of the car
def homePositionHorizontalServo():
    angleServo1.start(6.5)

#homePositionHorizontalServo()


def inputValueForHorizontalServo():
    #input value best from 4 to 8
    inputAngleServoCameraHorizontallyString = input("Please enter a string:\n")
    inputAngleServoCameraHorizontally = float(inputAngleServoCameraHorizontallyString)

    # Move camera to the home position
    angleServo1.ChangeDutyCycle(0.0)
    angleServo2.ChangeDutyCycle(0.0)

   
def moveHorizontalServoUpOrDown():

    angleServo1.start(inputAngleServoCameraHorizontally)
    angleServo1.ChangeDutyCycle(0.0)
    angleServo2.ChangeDutyCycle(0.0)
    # clean
    angleServo1.stop() 
    angleServo2.stop() 
    



    #moveHorizontalServoUpOrDown()

    #angleServo1.start(6.5)
    #angleServo1.start(6.5)

    #angleServo1.start(6.5)
    #angleServo2.start(6.5)
    #time.sleep(3)

    #Move camera left
    '''
    angleServo1.ChangeDutyCycle(4)
    angleServo2.ChangeDutyCycle(0)
    time.sleep(0.5)
    angleServo1.ChangeDutyCycle(0)
    time.sleep(3)

    angleServo1.ChangeDutyCycle(4)
    angleServo2.ChangeDutyCycle(0)
    time.sleep(0.5)
    angleServo1.ChangeDutyCycle(0)
    time.sleep(3)

    angleServo1.ChangeDutyCycle(0)
    angleServo2.ChangeDutyCycle(4)
    time.sleep(0.5)
    angleServo2.ChangeDutyCycle(0)
    time.sleep(3)

    angleServo1.ChangeDutyCycle(0)
    angleServo2.ChangeDutyCycle(8)
    time.sleep(0.5)
    angleServo2.ChangeDutyCycle(0)
    time.sleep(3)


    '''




# clean
#angleServo1.stop()
#angleServo2.stop()
#GPIO.cleanup()