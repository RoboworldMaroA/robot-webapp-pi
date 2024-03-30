# 4dc controle by webapp using FLASK
#

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
#for line follower
from picamera.array import PiRGBArray


#app = Flask(__name__)

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
#print("use navigation in menu on the web server to run a car")
#input("Press enter to continue and open http:..... link what you will se for a second in chromium web broswer")

'''
# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
/
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

try:
        while True:
            print("You can controll by using up down left right")
            print('press enter to stop press q to exit')
            char = screen.getch()
            if char == ord('q'):

                break
            elif char == curses.KEY_UP:
                print("run forward -u pressed up")
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                p1.ChangeDutyCycle(55)
                time.sleep(0.5)
                p1.ChangeDutyCycle(23)
                
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
                p2.ChangeDutyCycle(55)
                time.sleep(0.5)
                p2.ChangeDutyCycle(23)
                
                

            elif char == curses.KEY_DOWN:
                print("backward - u pressed down")
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                p1.ChangeDutyCycle(30)
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
                p2.ChangeDutyCycle(30)

            elif char == curses.KEY_RIGHT:
                print("turn right - u pressed right")
                #right motors reverse low speed
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                p1.ChangeDutyCycle(8)
                #left motors forvward
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
                p2.ChangeDutyCycle(80)


            elif char == curses.KEY_LEFT:
                print("turn left - u pressed left")
                #right motors forward
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                p1.ChangeDutyCycle(70)
                #left motors forward very slow
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
                p2.ChangeDutyCycle(8)



            elif char == 10:
                print("stop - u pressed enter")
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW)

finally:
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    GPIO.cleanup()




'''






#decorator to disply web in we broswer window


#video = cv2.VideoCapture(0)
app = Flask(__name__)
'''
for ip camera use - rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' 
for local webcam use cv2.VideoCapture(0)
'''
#it is good program I am going to modify this to add line follower
def video_stream():
    video = cv2.VideoCapture(0)
    
    while True:
        ret, frame = video.read()  # read the camera frame
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpeg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


'''

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
'''
#when operator press line follower camera then turn off what is in the video stream and display new stream from program for  line following window from camera 
   


  
#tell flask what is a main website, webbapp
@app.route('/') 
def home(username=None, post_id=None):
    return render_template('./camera.html', name=username)

#tis will be camrera.html seperate website for test only
@app.route('/camera') 
def camera():
    return render_template('./camera.html')

@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


#when I use this server camera is displayed in my web browswer, this server is executed inside the python file
# I am going to tty run this from outside server, when I activare server from command lines then is diffent Ip address
#when I tryed then I have got error, i think i should run in the serever started from python file
#app.run(host='0.0.0.0', port='5000', debug=False) I moved this line to the end of the file


'''
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
'''
'''
@app.route('/camera.html')
def camera_on(username=None, post_id=None):
    camera = PiCamera()
    camera.rotation = 0
    camera.start_preview()
    sleep(10)
    camera.stop_preview()
    camera.close()
    if camera == True:
        print("it is reading no need to wait");
    else:
        print("No transfering video");
    return render_template('./controller.html', name=username)


'''

@app.route('/forward.html')
def forward(username=None, post_id=None):
    print("run forward -u pressed up")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    p1.ChangeDutyCycle(99)
    p2.ChangeDutyCycle(99)
    
    time.sleep(0.15)
    p1.ChangeDutyCycle(30)
    p2.ChangeDutyCycle(30)
    
    time.sleep(9)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
   


    return render_template('./camera.html', name=username)


@app.route('/stop.html')
def stop(username=None, post_id=None):
    print("run forward -u pressed up")
    print("stop - u pressed enter")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    return render_template('./camera.html', name=username)

@app.route('/backward.html')
def backward(username=None, post_id=None):
    print("backward - u pressed down")
    #right motors backward
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    p1.ChangeDutyCycle(80)
    #left motors backward
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    p2.ChangeDutyCycle(80)
    
    #wait for 1.5 second
    time.sleep(0.2)
    p1.ChangeDutyCycle(40)
    p2.ChangeDutyCycle(40) 
    
     #wait for 1.5 second
    time.sleep(0.8)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    
    
    
    
    return render_template('./camera.html', name=username)



@app.route('/turn_left.html')
def left(username=None, post_id=None):
    print("turn left - u pressed left")
    #right motors forward
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
  
    #left motors forward very slow
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    #speed
    p1.ChangeDutyCycle(90)
    p2.ChangeDutyCycle(0)
    
    #turn left for 1.5 second
    time.sleep(1.0)
    
    
    #right motors backward
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    p1.ChangeDutyCycle(0)
    #left motors backward
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    p2.ChangeDutyCycle(80)
    
    
    time.sleep(1.5)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    
    return render_template('./camera.html', name=username)

@app.route('/turn_right.html')
def right(username=None, post_id=None):
    print("turn right - u pressed right")
    #right motors reverse low speed
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    p1.ChangeDutyCycle(0)
    #left motors forvward
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    p2.ChangeDutyCycle(100)
     #turn left for 1.5 second
    time.sleep(1.0)
    
    #right motors backward
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    p1.ChangeDutyCycle(80)
    #left motors backward
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    p2.ChangeDutyCycle(0)
    
    
    time.sleep(1.1)
    
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    p1.ChangeDutyCycle(0)
    #left motors forvward
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    p2.ChangeDutyCycle(0)
    
    return render_template('./camera.html', name=username)

@app.route('/camera.html') 
def camera_on():
    return render_template('./camera.html')


'''
@app.route('/controller.html') 
def index(username=None, post_id=None):
    return render_template('./controller.html', name=username)
'''




@app.route('/auto_Drive.html')
def auto(username=None, post_id=None):
    print("run auto when -u pressed button Auto Drive")
    
   
    #Forward
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    p1.ChangeDutyCycle(99)
    p2.ChangeDutyCycle(99)
    
    time.sleep(0.15)
    p1.ChangeDutyCycle(35)
    p2.ChangeDutyCycle(35)
    
    time.sleep(5)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
   
    #Turn around 2 times turn right
    #right motors reverse low speed
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    p1.ChangeDutyCycle(0)
    #left motors forvward
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    p2.ChangeDutyCycle(100)
     #turn left for 1.5 second
    time.sleep(1.4) 
    #right motors backward
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    p1.ChangeDutyCycle(90)
    #left motors backward
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    p2.ChangeDutyCycle(0)
    time.sleep(1.1)
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    p1.ChangeDutyCycle(0)
    #left motors forvward
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    p2.ChangeDutyCycle(0)
    
    
    #turn again
    #right motors reverse low speed
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    p1.ChangeDutyCycle(0)
    #left motors forvward
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    p2.ChangeDutyCycle(100)
     #turn left for 1.5 second
    time.sleep(1.4) 
    #right motors backward
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    p1.ChangeDutyCycle(80)
    #left motors backward
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    p2.ChangeDutyCycle(0)
    time.sleep(1.1)
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    p1.ChangeDutyCycle(0)
    #left motors forvward
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    p2.ChangeDutyCycle(0)
    
    
    #Go Forward
    
    #Forward
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    p1.ChangeDutyCycle(99)
    p2.ChangeDutyCycle(99)
    
    time.sleep(0.15)
    p1.ChangeDutyCycle(40)
    p2.ChangeDutyCycle(40)
    
    time.sleep(5)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    
    #go backward
    #right motors backward
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    p1.ChangeDutyCycle(80)
    #left motors backward
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    p2.ChangeDutyCycle(80)
    
    #wait for 1.5 second
    time.sleep(2.2)
    p1.ChangeDutyCycle(80)
    p2.ChangeDutyCycle(80) 
    
     #wait for 1.5 second
    time.sleep(0.2)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    
    
    #Forward Fast
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    p1.ChangeDutyCycle(99)
    p2.ChangeDutyCycle(99)
    
    time.sleep(1.0)
    p1.ChangeDutyCycle(99)
    p2.ChangeDutyCycle(99)
    
    time.sleep(0.9)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)

    
    #stop
    #right wheels
    p1.ChangeDutyCycle(0)
    #left wheels
    p2.ChangeDutyCycle(0)
    
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)



    return render_template('./camera.html', name=username)






















@app.route('/line_tracker.html')
def line_tracker():
        # Initialize camera
    camera = PiCamera()
    camera.resolution = (192,108)
    camera.framerate = 20
    rawCapture = PiRGBArray(camera,size=(192,108))
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
        #something, contours, hierarchy = cv2.findContours(mask.copy(),1,cv2.CHAIN_APPROX_NONE)
        contours, hierarchy = cv2.findContours(mask.copy(),1,cv2.CHAIN_APPROX_NONE)

        # Find x-axis centroid of largest contour and cut power to appropriate motor
        # to recenter camera on centroid.
        # This control algorithm was written referencing guide:
            # Author: Einsteinium Studios
            # Availability: http://einsteiniumstudios.com/beaglebone-opencv-line-following-robot.html
        if len(contours) > 0:
            # Find largest contour area and image moments
            c = max(contours, key = cv2.contourArea)
            M = cv2.moments(c)

            # Find x-axis centroid using image moments
            cx = int(M['m10']/M['m00'])
            
            if cx >= 150:
                print("Turn left")
                #right motors forward
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                p1.ChangeDutyCycle(70)
                #left motors forward very slow
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
                p2.ChangeDutyCycle(8)
            if cx < 150 and cx > 40:
                print("On Track!")
                print("run forward")
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                p1.ChangeDutyCycle(55)
                time.sleep(0.5)
                p1.ChangeDutyCycle(23)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
                p2.ChangeDutyCycle(55)
                time.sleep(0.5)
                p2.ChangeDutyCycle(23)
            if cx <= 40:
                print("Turn Right")
                #right motors reverse low speed
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                p1.ChangeDutyCycle(8)
                #left motors forvward
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
                p2.ChangeDutyCycle(80) 

        if key == ord("q"):
                break

        rawCapture.truncate(0)
      
    
    return render_template('./camera.html')
    
    
app.run(host='0.0.0.0', port='5000', debug=False)

GPIO.cleanup()