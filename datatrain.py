import os
import cv2
import numpy as np
from PIL import Image

# Create a recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'dataSet'

# Function to get the images and their corresponding IDs
def getImagesWithID(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
    faces = []
    IDs = []
    
    for imagePath in imagePaths:
        try:
            # Convert image to grayscale
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg, 'uint8')
            
            # Extract ID from the image filename
            ID = int(os.path.split(imagePath)[-1].split('.')[1])
            
            # Append the face data and IDs to their respective lists
            faces.append(faceNp)
            IDs.append(ID)
            
            # Display the face being trained
            cv2.imshow('training', faceNp)
            cv2.waitKey(10)
        
        except Exception as e:
            print(f"Error processing file {imagePath}: {e}")
    
    return np.array(IDs), faces

# Get faces and their corresponding IDs
Ids, faces = getImagesWithID(path)

# Train the recognizer with the faces and IDs
recognizer.train(faces, Ids)

# Create the trainer folder if it doesn't exist
if not os.path.exists('trainer'):
    os.makedirs('trainer')

# Save the trained model
recognizer.save('recognizer/training_data.yml')

# Close all windows
cv2.destroyAllWindows()
