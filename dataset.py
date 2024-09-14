import numpy as np
import cv2

# Membuka kamera
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("Error: Camera not accessible")
    exit()

# Load classifier Haarcascade untuk deteksi wajah
faceDetect = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

# Input ID pengguna
id = input('Enter user ID: ')
sampleNum = 0

while True:
    # Membaca frame dari kamera
    ret, img = cam.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Mengubah gambar menjadi grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Deteksi wajah
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    
    # Menyimpan wajah yang terdeteksi dan menggambar kotak
    for (x, y, w, h) in faces:
        sampleNum += 1
        cv2.imwrite("dataSet/User." + str(id) + "." + str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.waitKey(100)

    # Menampilkan frame dengan wajah yang dilingkari
    cv2.imshow("Face", img)

    # Jika jumlah sampel sudah sama dengan 50, hentikan
    if sampleNum == 50:
        break

    cv2.waitKey(1)

# Menutup kamera dan jendela
cam.release()
cv2.destroyAllWindows()
