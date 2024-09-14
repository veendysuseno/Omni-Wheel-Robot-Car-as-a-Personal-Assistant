import numpy as np
import os
import time
import cv2
from flask import Flask, render_template, Response
from datetime import datetime
import motor as motor
import pyttsx3

app = Flask(__name__)

# Inisialisasi background subtractor dan engine suara
sub = cv2.createBackgroundSubtractorMOG2()  # create background subtractor
engine = pyttsx3.init()
engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")  # set voice type
engine.setProperty('rate', 100)  # kecepatan baca suara

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen():
    """Video streaming generator function."""
    cap = cv2.VideoCapture(0)
    faceDetect = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
    rec = cv2.face.LBPHFaceRecognizer_create()
    rec.read("recognizer/training_data.yml")

    i = 0  # Variable untuk mengelola indeks file video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output'+str(i)+'.avi', fourcc, 10.0, (640, 480))

    last_text = ""  # Menyimpan teks sebelumnya untuk mencegah pengulangan ucapan

    while cap.isOpened():
        ret, frame = cap.read()  # Baca frame dari kamera
        if not ret:  # Jika frame tidak terbaca, ulangi
            cap = cv2.VideoCapture(0)
            continue

        # Konversi ke grayscale untuk deteksi wajah
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)

        # Tampilkan waktu pada frame
        cv2.putText(frame, str(datetime.now()), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2, cv2.LINE_AA)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 4)

            id, conf = rec.predict(gray[y:y+h, x:x+w])  # Prediksi wajah
            if id == 1:
                text = "VEENDY"
            else:
                text = "UNKNOWN"

            # Ucapkan nama hanya jika teks berubah
            if text != last_text:
                engine.say(text)
                engine.runAndWait()
                last_text = text  # Update teks terakhir

            cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2, cv2.LINE_AA)

            # Kontrol motor berdasarkan posisi wajah
            full = w + h
            tengah = x + (w / 2)

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

            # Simpan frame ke video output
            if os.path.exists("output" + str(i) + ".avi"):
                i += 1
            out.write(frame)

        # Encode frame untuk streaming
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Break jika 'q' ditekan
            break

    motor.cleanup()  # Bersihkan motor
    cap.release()  # Lepaskan kamera
    out.release()  # Simpan video
    cv2.destroyAllWindows()  # Tutup semua jendela

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
