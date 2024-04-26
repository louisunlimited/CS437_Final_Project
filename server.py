from flask import Flask, Response
import picamera2 as pic2
import cv2
import os
import pickle
from dotenv import load_dotenv

load_dotenv()

app = Flask("FinalProject")

# Load the model from pickle file
with open('face_model.pickle', 'rb') as file:
    face_model = pickle.load(file)

camera = pic2.Picamera2()
camera_config = camera.create_preview_configuration()
camera.configure(camera_config)
camera.start_preview(pic2.Preview.NULL)
camera.start()

def generate_frames():
    while True:
        frame = camera.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

        # Use the model to detect faces
        faces = face_model.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host=os.getenv("SERVER_HOST"), port=os.getenv("SERVER_PORT"), debug=False, threaded=True)
