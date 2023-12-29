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
#print("use nawigation in menu on the web server to run a car")
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


video = cv2.VideoCapture(0)
app = Flask(__name__)
'''
for ip camera use - rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' 
for local webcam use cv2.VideoCapture(0)
'''

def video_stream():
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
    p1.ChangeDutyCycle(55)
    time.sleep(0.5)
    p1.ChangeDutyCycle(23)

    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    p2.ChangeDutyCycle(55)
    time.sleep(0.5)
    p2.ChangeDutyCycle(23)
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
    p2.ChangeDutyCycle(40)
    return render_template('./camera.html', name=username)



@app.route('/turn_left.html')
def left(username=None, post_id=None):
    print("turn left - u pressed left")
    #right motors forward
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    p1.ChangeDutyCycle(70)
    #left motors forward very slow
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    p2.ChangeDutyCycle(8)
    return render_template('./camera.html', name=username)

@app.route('/turn_right.html')
def right(username=None, post_id=None):
    print("turn right - u pressed right")
    #right motors reverse low speed
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    p1.ChangeDutyCycle(8)
    #left motors forvward
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    p2.ChangeDutyCycle(80) 
    return render_template('./camera.html', name=username)

@app.route('/camera.html') 
def camera_on():
    return render_template('./camera.html')


'''
@app.route('/controller.html') 
def index(username=None, post_id=None):
    return render_template('./controller.html', name=username)
'''

app.run(host='0.0.0.0', port='5000', debug=False)

GPIO.cleanup()