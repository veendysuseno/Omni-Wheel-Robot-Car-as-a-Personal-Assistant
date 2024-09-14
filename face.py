import numpy as np
import cv2
import motor as motor
import time

# Inisialisasi kamera dan deteksi objek menggunakan haarcascade
cam = cv2.VideoCapture(0)
ball_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

b = 0  # Variabel untuk menghitung objek yang terdeteksi

while True:
    Cball = 0
    ret, img = cam.read()
    
    if not ret:
        break
    
    # Konversi gambar menjadi grayscale untuk deteksi objek
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ball = ball_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in ball:
        # Gambarkan kotak di sekitar objek yang terdeteksi
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        full = w + h
        tengah = x + (w / 2)
        print(f"Posisi x: {tengah}, Ukuran: {full}")
        
        # Logika pergerakan motor
        if tengah < 270:  # Jika objek ada di kiri
            motor.turnLeft()
            time.sleep(0.5)  # Kurangi delay untuk respons lebih cepat
            motor.stop()
            b += 1  # Tambahkan hitungan objek saat motor bergerak
        elif tengah > 370:  # Jika objek ada di kanan
            motor.turnRight()
        else:
            motor.stop()

        if full > 470:  # Jika objek terlalu dekat
            motor.backward()
        elif full < 430:  # Jika objek terlalu jauh
            motor.forward()
        else:
            motor.stop()

    # Tampilkan jumlah objek yang terdeteksi pada frame
    cv2.putText(img, "Objects detected: " + str(b), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2, cv2.LINE_AA)    
    
    # Tampilkan frame hasil
    cv2.imshow('frame', img)
    
    # Berhenti jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bersihkan resource setelah loop selesai
motor.cleanup()
cam.release()
cv2.destroyAllWindows()
