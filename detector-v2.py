import numpy as np
import cv2
import os
from datetime import datetime
import motor  # Pastikan modul ini tersedia dan berfungsi

# Inisialisasi kamera
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("Error: Kamera tidak dapat diakses")
    exit()

# Inisialisasi deteksi wajah
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
if faceDetect.empty():
    print("Error: File haarcascade_frontalface_default.xml tidak ditemukan")
    exit()

# Inisialisasi pengenal wajah
rec = cv2.face.LBPHFaceRecognizer_create()
if not os.path.exists("recognizer/training_data.yml"):
    print("Error: Model pengenalan wajah tidak ditemukan")
    exit()
rec.read("recognizer/training_data.yml")

# Pengaturan penulisan video
i = 0
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_filename = f'output{i}.avi'
while os.path.exists(output_filename):
    i += 1
    output_filename = f'output{i}.avi'
out = cv2.VideoWriter(output_filename, fourcc, 10.0, (640, 480))

try:
    while True:
        ret, img = cam.read()
        if not ret:
            print("Error: Gagal membaca frame dari kamera")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(img, timestamp, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            tengah = x + (w / 2)
            id, conf = rec.predict(gray[y:y + h, x:x + w])

            if id == 1:
                text = "VEENDY"
                print(f"Posisi x: {tengah}")
                # Kontrol motor berdasarkan posisi wajah
                if tengah < 270:
                    motor.turnLeft()
                elif tengah > 370:
                    motor.turnRight()
                else:
                    motor.stop()
            else:
                text = "UNKNOWN"

            cv2.putText(img, text, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2, cv2.LINE_AA)

        out.write(img)
        cv2.imshow('frame', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Program dihentikan oleh pengguna")
finally:
    # Membersihkan dan menutup semua sumber daya
    motor.cleanup()
    cam.release()
    out.release()
    cv2.destroyAllWindows()
