import numpy as np
import cv2
import os
import time
from datetime import datetime
import motor as motor

# Inisialisasi kamera dan detektor wajah
cam = cv2.VideoCapture(0)
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read("recognizer/training_data.yml")

# Video writer setup
i = 0
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output'+str(i)+'.avi', fourcc, 10.0, (640, 480))

while True:
    ret, img = cam.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)

    # Tampilkan tanggal dan waktu saat ini pada video
    cv2.putText(img, str(datetime.now()), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        full = w + h
        tengah = x + (w / 2)

        # Prediksi wajah
        id, conf = rec.predict(gray[y:y+h, x:x+w])

        if id == 1:
            text = "VEENDY"
            print("Posisi x :", str(tengah))
            print("Full: " + str(full))

            # Kontrol motor berdasarkan posisi wajah
            if tengah < 270:
                motor.turnLeft()
            elif tengah > 370:
                motor.turnRight()
            else:
                motor.stop()
        else:
            text = "UNKNOWN"

        # Tampilkan nama yang dikenali di atas wajah yang terdeteksi
        cv2.putText(img, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2, cv2.LINE_AA)

    out.write(img)
    cv2.imshow('frame', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Membersihkan sumber daya
motor.cleanup()
cam.release()
out.release()
cv2.destroyAllWindows()
