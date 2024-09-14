import numpy as np
import os
import time
import cv2 
from flask import Flask, render_template, Response
from datetime import datetime
import motor as motor
import pyttsx3

app = Flask(__name__)
sub = cv2.createBackgroundSubtractorMOG2()  # create background subtractor

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    cap = cv2.VideoCapture(0)
    faceDetect=cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
    rec=cv2.face.LBPHFaceRecognizer_create()
    rec.read("recognizer/training_data.yml")
    i = 0
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output'+str(i)+'.avi', fourcc, 10.0, (640,480))
    engine = pyttsx3.init() 
    engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")    #set voice type
    engine.setProperty('rate', 100)  ### 10 adalah kecepatan baca
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
    # Read until video is completed
    while(cap.isOpened()):
        ret, frame = cap.read()  # import image
        if not ret: #if vid finish repeat
            cap = cv2.VideoCapture(0)
            continue
        if ret:  # if there is a frame continue with code
            faceDetect=cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # converts image to gray
            faces= faceDetect.detectMultiScale(gray, 1.3, 5)
            cv2.putText(frame, str(datetime.now()), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255),2,cv2.LINE_AA)
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),4)        #cv2.imshow("countours", image)
                id,conf=rec.predict(gray[y:y+h,x:x+w])
                if(id==1):
                    text="ILHAM"
                    engine.say(text)
                    engine.runAndWait()
                else:
                    text="UNKNOWN"
                    engine.say(text)
                    engine.runAndWait()
                cv2.putText(frame, text, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255),2,cv2.LINE_AA)
                if os.path.exists("output"+str(i)+".avi"):
                    i += 1
                out.write(frame)
                full =w+h
                tengah =x+(w/2)
                print("posisi x :", str(tengah))
                print("full"+str(full))
                if tengah < 270:
                    motor.turnLeft()
                elif tengah > 370:
                    motor.turnRight()
                else:
                    motor.stop()

                if full > 470:
                    motor.backward()
                elif full < 430:
                    motor.forward()
                else:
                    motor.stop()

        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        #time.sleep(0.1)
        key = cv2.waitKey(20)
        if key == 27:
            break
    motor.cleanup()

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
	app.run(host = '0.0.0.0', debug=True)


    

