import numpy as np
import cv2
import os
import datetime
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="face.csv",
	help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

# Initialize camera and face detector
cam = cv2.VideoCapture(0)
faceDetect = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

# Initialize the recognizer
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read("recognizer/training_data.yml")

# Video writer setup
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_index = 0
output_file = f'vid/output{output_index}.avi'
while os.path.exists(output_file):
    output_index += 1
    output_file = f'vid/output{output_index}.avi'
out = cv2.VideoWriter(output_file, fourcc, 10.0, (640, 480))

# Open CSV file for logging recognized faces
csv = open(args["output"], "w")
found = set()

while True:
    ret, img = cam.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        id, conf = rec.predict(gray[y:y+h, x:x+w])

        # Recognize the ID and map it to the name
        if id == 1:
            text = "VEENDY"
        else:
            text = "UNKNOWN"

        # Log the recognition result into the CSV file
        if text not in found:
            csv.write(f"{datetime.datetime.now()},{text}\n")
            csv.flush()  # Ensure data is written to file
            found.add(text)

        # Display the name of the recognized person on the frame
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 3)

    out.write(img)
    cv2.imshow('frame', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
csv.close()
cam.release()
out.release()
cv2.destroyAllWindows()
