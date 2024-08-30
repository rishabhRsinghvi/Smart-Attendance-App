# Cell 3: Import necessary libraries
from ultralytics import YOLO
from ultralytics.engine.results import Results
from deepface import DeepFace
from PIL import Image
import gradio as gr
import shutil
import pandas as pd
import cv2
import os
from datetime import datetime
from mtcnn import MTCNN
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Cell 4: Define face recognition function
def faceRecognition(cropped_objects_dir):
    extracted_names = []
    predicted_image_filenames = []
    for filename in os.listdir(cropped_objects_dir):
        if filename.endswith(".jpg"):
            img_path = os.path.join(cropped_objects_dir, filename)
            model = DeepFace.find(img_path=img_path, db_path="uploads/attendancesystem/database", enforce_detection=False, model_name="ArcFace")
            if not model.empty:  # Check if a face was recognized
                name = model['identity'][0].split('/')[-2]
                extracted_names.append(name)
                predicted_image_filenames.append(filename)
            else:
                extracted_names.append('unknown')
                predicted_image_filenames.append(filename)
    return extracted_names, predicted_image_filenames

# Cell 5: Define face extraction function
def faceExtraction(input_image, results):
    detected_faces = []
    if results:
        for result in results:
            x, y, width, height = result['box']
            x1, y1, x2, y2 = x, y, x + width, y + height
            detected_faces.append((x1, y1, x2, y2))
    if os.path.exists("uploads/faces"):
        shutil.rmtree("uploads/faces")
    os.makedirs("uploads/faces")
    for i, (x1, y1, x2, y2) in enumerate(detected_faces):
        face_image = input_image[y1:y2, x1:x2]
        cv2.imwrite(f"uploads/faces/face{i}.jpg", face_image)
    return detected_faces

# Cell 6: Define face detection function
def faceDetection(input_image):
    detector_mtcnn = MTCNN()
    results = detector_mtcnn.detect_faces(input_image)
    return faceExtraction(input_image, results)

# Cell 7: Initialize webcam and process video
video_capture = cv2.VideoCapture(0)  # Use 0 for webcam, or provide the path to a video file
while True:
    ret, frame = video_capture.read()
    if not ret:
        break
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    detected_faces = faceDetection(small_frame)
    names, _ = faceRecognition("uploads/faces")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for (x1, y1, x2, y2), name in zip(detected_faces, names):
        x1, y1, x2, y2 = [v * 4 for v in (x1, y1, x2, y2)]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"{name} - {timestamp}", (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()
