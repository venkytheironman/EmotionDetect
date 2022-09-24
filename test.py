from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
from random import randrange

# To Load Harcascade Files
face_classifier = cv2.CascadeClassifier('/home/aniketh/Projects/Detection/haarcascade_frontalface_default.xml')
classifier = load_model('/home/aniketh/Projects/Detection/Emotion_Detection.h5')

class_labels = ['Angry','Happy','Neutral','Sad','Suprise']

# To Access the Web Cam
cap = cv2.VideoCapture(0)

while True:
    # Grab a single fram of video
    ret, frame = cap.read()
    labels = []
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    
    # For Rectangle Around Face 
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (randrange(256),randrange(256),randrange(256)), 4)
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)
        
        if np.sum([roi_gray])!=0:
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            
        # make a preiction on the ROI, then lookup the class
        
            preds = classifier.predict(roi)[0]
            print("\nprediction = ",preds)
            label = class_labels[preds.argmax()]
            print("\nprediction max = ",preds.argmax())
            print("\nlabel = ",label)
            label_position = (x,y)
            cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
        else:
            cv2.putText(frame,'No Face Found',(20,60),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
        print("\n\n")
    cv2.imshow('Emotion Detector',frame)
    # For Quiting the Window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()     


