

#This applicaion is recognise line using camera pi
# activate virtual env for webapp_robot and run comand python lineTracker3.py
#This version is 28Jan2024
#Marek Augustyn - Roboworld.pl

from picamera.array import PiRGBArray
import curses
import RPi.GPIO as GPIO
from flask import Flask, render_template, url_for, request, redirect, Response, stream_with_context
import csv
import numpy as np
import imutils
import cv2
import time
from picamera import PiCamera
from time import sleep


app = Flask(__name__)




# It is configuration Inpu and outup for my robot
in1 = 24 #right motor
in2 = 23
ena = 25
temp1=1

in3 = 17
in4 = 27
enb = 22


GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)


GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p1=GPIO.PWM(ena,1000)
p1.start(40)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p2=GPIO.PWM(enb,1000)
p2.start(40)


#video_capture = cv2.VideoCapture(0)
#video_capture.set(3, 160)
#video_capture.set(4, 120)

# Initialize camera
camera = PiCamera()
camera.resolution = (240,240)
camera.framerate = 20
rawCapture = PiRGBArray(camera,size=(240,240))
time.sleep(0.1)
 
# Loop over all frames captured by camera indefinitely
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

	# Display camera input
	image = frame.array
	cv2.imshow('img',image)

	# Create key to break for loop
	key = cv2.waitKey(1) & 0xFF

	# convert to grayscale, gaussian blur, and threshold
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(5,5),0)
	ret,thresh1 = cv2.threshold(blur,100,255,cv2.THRESH_BINARY_INV)

	# Erode to eliminate noise, Dilate to restore eroded parts of image
	mask = cv2.erode(thresh1, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# Find all contours in frame
	something, contours, hierarchy = cv2.findContours(mask.copy(),1,cv2.CHAIN_APPROX_NONE)
# 	contours, hierarchy = cv2.findContours(mask.copy(),1,cv2.CHAIN_APPROX_NONE)

	# Find x-axis centroid of largest contour and cut power to appropriate motor
	# to recenter camera on centroid.
	# This control algorithm was written referencing guide:
		# Author: Einsteinium Studios
		# Availability: http://einsteiniumstudios.com/beaglebone-opencv-line-following-robot.html
# 	print("Contour length")
# 	print(contours)
	if len(contours) > 0:
		# Find largest contour area and image moments
		c = max(contours, key = cv2.contourArea)
		M = cv2.moments(c)

		# Find x-axis centroid using image moments
		cx = int(M['m10']/M['m00'])
		print("centroid value")
		print(cx)
		
		if cx <= 62:
			print("Back find a line")
			#right motors back
			GPIO.output(in1,GPIO.HIGH)
			GPIO.output(in2,GPIO.LOW)
			p1.ChangeDutyCycle(80)
			#left motors back
			GPIO.output(in3,GPIO.HIGH)
			GPIO.output(in4,GPIO.LOW)
			p2.ChangeDutyCycle(80)
			time.sleep(0.2)
			
		if cx <= 89 and cx > 52:
			print("Turn medium left")
			#right motors forward
			GPIO.output(in1,GPIO.LOW)
			GPIO.output(in2,GPIO.HIGH)
			p1.ChangeDutyCycle(90)
			#left motors stop
			GPIO.output(in3,GPIO.HIGH)
			GPIO.output(in4,GPIO.LOW)
			p2.ChangeDutyCycle(0)
			time.sleep(0.001)
		
		if cx <= 120 and cx > 89:
			print("Turn slow left")
			#right motors forward
			GPIO.output(in1,GPIO.LOW)
			GPIO.output(in2,GPIO.HIGH)
			p1.ChangeDutyCycle(90)
			#left motors stop
			GPIO.output(in3,GPIO.HIGH)
			GPIO.output(in4,GPIO.LOW)
			p2.ChangeDutyCycle(0)
			time.sleep(0.001)
			
		#FORWARD
		if cx < 130 and cx > 110:
			print("On Track!")
			print("run forward")
			GPIO.output(in1,GPIO.LOW)
			GPIO.output(in2,GPIO.HIGH)
			p1.ChangeDutyCycle(85)
			GPIO.output(in3,GPIO.LOW)
			GPIO.output(in4,GPIO.HIGH)
			p2.ChangeDutyCycle(85)
			time.sleep(0.02)
			
		if cx >= 140 and cx < 170:
			print("Turn slow to the Right")
			#right motors reverse low speed
			GPIO.output(in1,GPIO.LOW)
			GPIO.output(in2,GPIO.HIGH)
			p1.ChangeDutyCycle(0)
			#left motors forward
			GPIO.output(in3,GPIO.LOW)
			GPIO.output(in4,GPIO.HIGH)
			p2.ChangeDutyCycle(80)
			time.sleep(0.001)
			
			
		if cx >= 170 and cx < 200:
			print("Turn medium to the Right")
			#right motors stopped
			GPIO.output(in1,GPIO.LOW)
			GPIO.output(in2,GPIO.HIGH)
			p1.ChangeDutyCycle(0)
			#left motors forward
			GPIO.output(in3,GPIO.LOW)
			GPIO.output(in4,GPIO.HIGH)
			p2.ChangeDutyCycle(80)
			
		if cx >= 165:
			print("Back find a line")
			#right motors back
			GPIO.output(in1,GPIO.HIGH)
			GPIO.output(in2,GPIO.LOW)
			p1.ChangeDutyCycle(80)
			#left motors back
			GPIO.output(in3,GPIO.HIGH)
			GPIO.output(in4,GPIO.LOW)
			p2.ChangeDutyCycle(80)
			time.sleep(0.2)
			

	if key == ord("q"):
            break

	rawCapture.truncate(0)

#clean GPIO at the end
GPIO.cleanup()






