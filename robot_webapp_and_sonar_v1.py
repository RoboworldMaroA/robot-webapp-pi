# 4dc controle by webapp using FLASK
# Marek Augustyn
# In this app added sonar HC-SR04, that robot stop if is 20cm from obstacle

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

# GPIO.cleanup()
GPIO.setwarnings(False)

#app = Flask(__name__)

# It is configuration Input and output L298N 
in1 = 24 #right motor
in2 = 23
ena = 25
temp1=1

#left motor
in3 = 17
in4 = 27
enb = 22

#variable for sonar
GPIO_TRIGGER = 20
GPIO_ECHO = 21

#Setup for DC motors
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

stopStatus = False


#setup GPIO fro sonar
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because signal must back to the sensor
    distance = (TimeElapsed * 34300) / 2
 
    return distance


dist = distance()
print ("Measured Distance = %.1f cm" % dist)


info = ""

if __name__ == '__main__':
    try:
        #while True:
        while stopStatus == False:    
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
            
            #Video Capture

            video = cv2.VideoCapture(0)
            app = Flask(__name__)
            
            if dist > 10:
                print("Distance is more that 20cm, so waiting for video and motors")
                # GPIO.output(in1,GPIO.LOW)
                # GPIO.output(in2,GPIO.HIGH)
                # p1.ChangeDutyCycle(35)
                # time.sleep(0.5)
                # p1.ChangeDutyCycle(35)

                # GPIO.output(in3,GPIO.LOW)
                # GPIO.output(in4,GPIO.HIGH)
                # p2.ChangeDutyCycle(35)
                # time.sleep(0.5)
                # p2.ChangeDutyCycle(35)




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
                def home(dist=dist, post_id=None):
                    return render_template('./camera.html', dist=dist)

                #main website
                @app.route('/camera') 
                def camera():
                    return render_template('./camera.html')

                @app.route('/video_feed')
                def video_feed():
                    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


                #when I use this server camera is displayed in my web browswer, this server is executed inside the python file
                # I am going to try run this from outside server, when I activare server from command lines then is diffent Ip address
                #when I tried then I have got error, i think i should run in the serever started from python file
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

                #Run the motors forward and stop if obstacle is 10 cm from the robot then robot wont go
    
                @app.route('/forward')
                def forward(dist=dist, post_id=None):
                    GPIO.setmode(GPIO.BCM)
                    print("forw 1")
                    dist2 = distance()
                    print(dist2)
                    if dist2 > 10:
                        print("run forward -u pressed up")
                        GPIO.output(in1,GPIO.LOW)
                        GPIO.output(in2,GPIO.HIGH)
                        p1.ChangeDutyCycle(35)
                     
                        #speed of the second motor
                        GPIO.output(in3,GPIO.LOW)
                        GPIO.output(in4,GPIO.HIGH)
                        p2.ChangeDutyCycle(35)
                     
                        print("forw 2")
                        dist3 =  distance()
                        print(dist3)
                    if dist2 < 10:
                        print("too close the obstacle")
                        GPIO.output(in1,GPIO.LOW)
                        GPIO.output(in2,GPIO.LOW)
                        GPIO.output(in3,GPIO.LOW)
                        GPIO.output(in4,GPIO.LOW)
                        # dist =  distance()
                        print(dist2)
                        
                    return render_template('./camera.html', dist=dist2)

                #This is forward second version. First version Robot recognize what is a distance from obstacle in the moment of the pressing the go button
                #I want to add a loop that it recognize all the time. Problem is that it is a function that is executed when we pressed the button go
                #so it does not checking again what is a distance later, only just go. So I have to add again function that will be reading a new vaue in the loop and
                # until the distace is bigger then 10 cm or user press stop but in this form robot wont stop

                @app.route('/forward2')
                def forward2(dist=None, post_id=None):
                    GPIO.setmode(GPIO.BCM)
                    print("display value of the first distance")
                    print(dist)

                    print("forw 11")
                    dist2 = distance()
                    print(dist2)

                    print(stopStatus)
                    while (dist > 20) or (stopStatus == False):
                        print("run forward -u pressed up")
                        GPIO.output(in1,GPIO.LOW)
                        GPIO.output(in2,GPIO.HIGH)
                        p1.ChangeDutyCycle(15)
                     

                        GPIO.output(in3,GPIO.LOW)
                        GPIO.output(in4,GPIO.HIGH)
                        p2.ChangeDutyCycle(15)
                     
                        print("forw 22")
                        dist3 =  distance()
                        print(dist3)
                        if dist3 < 10:
                            print("too close the obstacle")
                            GPIO.output(in1,GPIO.LOW)
                            GPIO.output(in2,GPIO.LOW)
                            GPIO.output(in3,GPIO.LOW)
                            GPIO.output(in4,GPIO.LOW)
                            p1.ChangeDutyCycle(0)
                            p2.ChangeDutyCycle(0)
                            dist3 = 41
                            dist2 = 41
                            break
                    
                    print("too close the obstacle out of loop")
                    GPIO.output(in1,GPIO.LOW)
                    GPIO.output(in2,GPIO.LOW)
                    GPIO.output(in3,GPIO.LOW)
                    GPIO.output(in4,GPIO.LOW)
                    dist4 =  distance()
                    print("Dist4 ")
                    print(dist4)
                        
                    return render_template('./camera.html', dist=dist4, )

                # STOP
                
                @app.route('/stop')
                def stop(username=None, post_id=None):

                    print("robot stop - u pressed stop")
                    GPIO.output(in1,GPIO.LOW)
                    GPIO.output(in2,GPIO.HIGH)
                    p1.ChangeDutyCycle(0)
                    
                    GPIO.output(in3,GPIO.LOW)
                    GPIO.output(in4,GPIO.HIGH)
                    p2.ChangeDutyCycle(0)


                    GPIO.output(in1,GPIO.LOW)
                    GPIO.output(in2,GPIO.LOW)
                    GPIO.output(in3,GPIO.LOW)
                    GPIO.output(in4,GPIO.LOW)
                    stopStatus = True
                    dist = 10
            
                    return render_template('./camera.html', name=username)
                
                #REVERSE
                # Driving a car reverse direction

                @app.route('/backward')
                def backward(username=None, post_id=None):
                    print("backward - u pressed down")
                    dist = distance()
                    print(dist)
                    if dist > 10:
                        #right motors backward
                        GPIO.output(in1,GPIO.HIGH)
                        GPIO.output(in2,GPIO.LOW)
                        p1.ChangeDutyCycle(80)
                        #left motors backward
                        GPIO.output(in3,GPIO.HIGH)
                        GPIO.output(in4,GPIO.LOW)
                        p2.ChangeDutyCycle(40)
                        info = "Safe to drive"
                        dist =  distance()
                        return render_template('./camera.html', dist=dist, info=info)
                         
                    if dist < 10:
                        print("too close the obstacle")
                        GPIO.output(in1,GPIO.LOW)
                        GPIO.output(in2,GPIO.LOW)
                        GPIO.output(in3,GPIO.LOW)
                        GPIO.output(in4,GPIO.LOW)
                        dist =  distance()
                        info = "Too close to the obstacle"
                        return render_template('./camera.html', dist=dist, info=info)

                #TURN LEFT
                @app.route('/turn_left')
                def left(dist=dist, info=info,  post_id=None):
                    print("turn left - u pressed left")
                    dist = distance()
                    print(dist)
                    if dist > 10:
                        #right motors forward
                        GPIO.output(in1,GPIO.LOW)
                        GPIO.output(in2,GPIO.HIGH)
                        p1.ChangeDutyCycle(70)
                        #left motors forward very slow
                        GPIO.output(in3,GPIO.HIGH)
                        GPIO.output(in4,GPIO.LOW)
                        p2.ChangeDutyCycle(8)
                        info = "Safe to drive"
                        return render_template('./camera.html', dist=dist, info=info)

                    
                    if dist < 10:
                        print("too close the obstacle")
                        GPIO.output(in1,GPIO.LOW)
                        GPIO.output(in2,GPIO.LOW)
                        GPIO.output(in3,GPIO.LOW)
                        GPIO.output(in4,GPIO.LOW)
                        dist =  distance()
                        info = "Too close to the obstacle"
                        return render_template('./camera.html', dist=dist, info=info)
                

                #TURN RIGHT    
                #This is simple version just go to the right and when you press stop then robot stop.
                #It store a distance from the obstacle and display info if is safe or not
                @app.route('/turn_right')
                def right(dist=dist, info=info, post_id=None):

                    print("turn right - u pressed right")
                    dist = distance()
                    print(dist)
                    if dist > 10:
                        #right motors reverse low speed
                        GPIO.output(in1,GPIO.HIGH)
                        GPIO.output(in2,GPIO.LOW)
                        p1.ChangeDutyCycle(8)
                        #left motors forvward
                        GPIO.output(in3,GPIO.LOW)
                        GPIO.output(in4,GPIO.HIGH)
                        p2.ChangeDutyCycle(80) 
                        info = "Safe to drive"
                        return render_template('./camera.html', dist=dist, info=info)

                    if dist < 10:
                        print("too close the obstacle")
                        GPIO.output(in1,GPIO.LOW)
                        GPIO.output(in2,GPIO.LOW)
                        GPIO.output(in3,GPIO.LOW)
                        GPIO.output(in4,GPIO.LOW)
                        dist =  distance()
                        info = "Too close to the obstacle"
                        return render_template('./camera.html', dist=dist, info=info)
          





                #Camera view

                @app.route('/camera') 
                def camera_on():
                    return render_template('./camera.html')
                


                ''' Autodrive '''

                @app.route('/auto-drive')
                def autoDrive(dist=dist, info=info, post_id=None):
                    print("You pressed auto drive")
                    dist = distance()
                    print(dist)
                    print(stopStatus)
                    if (dist > 10):
                        #right motors forward
                        GPIO.output(in1,GPIO.LOW)
                        GPIO.output(in2,GPIO.HIGH)
                        p1.ChangeDutyCycle(1)
                        #left motors forward very slow
                        GPIO.output(in3,GPIO.HIGH)
                        GPIO.output(in4,GPIO.LOW)
                        p2.ChangeDutyCycle(1)

                        #autodrive program

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
                        #End Autodrive read distance
                        dist =  distance()
                        info = "Autodrive cycle has been completed"
                        return render_template('./camera.html', dist=dist, info=info)

                        
                    if (dist < 10):
                        print("too close the obstacle in autodrive mode")
                        p1.ChangeDutyCycle(0)
                        p2.ChangeDutyCycle(0)
                        
                        GPIO.output(in1,GPIO.LOW)
                        GPIO.output(in2,GPIO.LOW)
                        GPIO.output(in3,GPIO.LOW)
                        GPIO.output(in4,GPIO.LOW)
                        dist =  distance()
                        info = "Too close to the obstacle"
                        return render_template('./camera.html', dist=dist, info=info)




                '''
                Autodrive with Emergency Stop
                I want to stup the cycle. It is long auto program I will be presing stop or extra buton reset and
                then it will be stopping all motors
                
                '''


                @app.route('/auto-drive')
                def autoDrive2(dist=dist, info=info, post_id=None):
                    print("You pressed auto drive")
                    dist = distance()
                    print(dist)
                    print(stopStatus)
                  
                    if (dist > 10):
                         while stopStatus == False:
                            #right motors forward
                            GPIO.output(in1,GPIO.LOW)
                            GPIO.output(in2,GPIO.HIGH)
                            p1.ChangeDutyCycle(1)
                            #left motors forward very slow
                            GPIO.output(in3,GPIO.HIGH)
                            GPIO.output(in4,GPIO.LOW)
                            p2.ChangeDutyCycle(1)

                            #autodrive program

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
                            #End Autodrive read distance
                            dist =  distance()
                            info = "Autodrive cycle has been completed"
                            return render_template('./camera.html', dist=dist, info=info)

                        
                    if (dist < 10):
                        print("too close the obstacle in autodrive mode")
                        p1.ChangeDutyCycle(0)
                        p2.ChangeDutyCycle(0)
                        
                        GPIO.output(in1,GPIO.LOW)
                        GPIO.output(in2,GPIO.LOW)
                        GPIO.output(in3,GPIO.LOW)
                        GPIO.output(in4,GPIO.LOW)
                        dist =  distance()
                        info = "Too close to the obstacle"
                        return render_template('./camera.html', dist=dist, info=info)






                '''
                @app.route('/controller.html') 
                def index(username=None, post_id=None):
                    return render_template('./controller.html', name=username)
                '''

                app.run(host='0.0.0.0', port='5000', debug=False)

                # GPIO.cleanup()
            
            #if robot distance from the ostacle is less then 20cm then stop the motors
            
            print("less than 20cm stop motors")
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.LOW)


        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        app.run(host='0.0.0.0', port='5000', debug=False)
        GPIO.setmode(GPIO.BCM)
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
        GPIO.cleanup()


print("last sentence")
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
GPIO.cleanup()

#print("use arrows on the web server to run a car")
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


# video = cv2.VideoCapture(0)
# app = Flask(__name__)
'''
for ip camera use - rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' 
for local webcam use cv2.VideoCapture(0)
'''

# def video_stream():
#     while True:
#         ret, frame = video.read()  # read the camera frame
#         if not ret:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpeg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


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
# @app.route('/') 
# def home(username=None, post_id=None):
#     return render_template('./camera.html', name=username)

# #tis will be camrera.html seperate website for test only
# @app.route('/camera') 
# def camera():
#     return render_template('./camera.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


#when I use this server camera is displayed in my web browswer, this server is executed inside the python file
# I am going to try run this from outside server, when I activare server from command lines then is diffent Ip address
#when I tried then I have got error, i think i should run in the serever started from python file
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

# @app.route('/forward')
# def forward(username=None, post_id=None):
#     print("run forward -u pressed up")
#     GPIO.output(in1,GPIO.LOW)
#     GPIO.output(in2,GPIO.HIGH)
#     p1.ChangeDutyCycle(35)
#     time.sleep(0.5)
#     p1.ChangeDutyCycle(35)

#     GPIO.output(in3,GPIO.LOW)
#     GPIO.output(in4,GPIO.HIGH)
#     p2.ChangeDutyCycle(35)
#     time.sleep(0.5)
#     p2.ChangeDutyCycle(35)
#     return render_template('./camera.html', name=username)


# @app.route('/stop')
# def stop(username=None, post_id=None):
#     print("run forward -u pressed up")
#     print("stop - u pressed enter")
#     GPIO.output(in1,GPIO.LOW)
#     GPIO.output(in2,GPIO.LOW)
#     GPIO.output(in3,GPIO.LOW)
#     GPIO.output(in4,GPIO.LOW)
#     return render_template('./camera.html', name=username)

# @app.route('/backward')
# def backward(username=None, post_id=None):
#     print("backward - u pressed down")
#     #right motors backward
#     GPIO.output(in1,GPIO.HIGH)
#     GPIO.output(in2,GPIO.LOW)
#     p1.ChangeDutyCycle(80)
#     #left motors backward
#     GPIO.output(in3,GPIO.HIGH)
#     GPIO.output(in4,GPIO.LOW)
#     p2.ChangeDutyCycle(40)
#     return render_template('./camera.html', name=username)



# @app.route('/turn_left')
# def left(username=None, post_id=None):
#     print("turn left - u pressed left")
#     #right motors forward
#     GPIO.output(in1,GPIO.LOW)
#     GPIO.output(in2,GPIO.HIGH)
#     p1.ChangeDutyCycle(70)
#     #left motors forward very slow
#     GPIO.output(in3,GPIO.HIGH)
#     GPIO.output(in4,GPIO.LOW)
#     p2.ChangeDutyCycle(8)
#     return render_template('./camera.html', name=username)

# @app.route('/turn_right')
# def right(username=None, post_id=None):
#     print("turn right - u pressed right")
#     #right motors reverse low speed
#     GPIO.output(in1,GPIO.HIGH)
#     GPIO.output(in2,GPIO.LOW)
#     p1.ChangeDutyCycle(8)
#     #left motors forvward
#     GPIO.output(in3,GPIO.LOW)
#     GPIO.output(in4,GPIO.HIGH)
#     p2.ChangeDutyCycle(80) 
#     return render_template('./camera.html', name=username)

# @app.route('/camera') 
# def camera_on():
#     return render_template('./camera.html')


# '''
# @app.route('/controller.html') 
# def index(username=None, post_id=None):
#     return render_template('./controller.html', name=username)
# '''

# app.run(host='0.0.0.0', port='5000', debug=False)

# GPIO.cleanup()