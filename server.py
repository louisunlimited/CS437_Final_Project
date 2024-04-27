from flask import Flask, Response
import picamera2 as pic2
import cv2
import os
import pickle
import face_recognition
from threading import Thread
from queue import Queue
import time

# Load environment variables
import dotenv
dotenv.load_dotenv()

app = Flask("FinalProject")

# Load the model from pickle file
print("[INFO] loading encodings + face detector...")
with open('louis.pickle', 'rb') as file:
    known_faces = pickle.load(file)

# Initialize and start the camera
camera = pic2.Picamera2()
camera_config = camera.create_preview_configuration()
camera.configure(camera_config)
camera.start_preview(pic2.Preview.NULL)
camera.start()

# Initialize a queue to handle frames
frame_queue = Queue()
result_queue = Queue()

def face_recognition_worker():
    while True:
        frame_rgb = frame_queue.get()
        if frame_rgb is None:
            break

        # Find face locations and face encodings in the current frame
        face_locations = face_recognition.face_locations(frame_rgb, model='hog')
        face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)

        results = []
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Check if the face is a match for known faces
            matches = face_recognition.compare_faces(known_faces['encodings'], face_encoding)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_faces['names'][first_match_index]

            results.append((top, right, bottom, left, name))
        
        result_queue.put(results)

def generate_frames():
    # Start the face recognition thread
    recognition_thread = Thread(target=face_recognition_worker)
    recognition_thread.start()

    while True:
        frame = camera.capture_array()
        out_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        frame_rgb = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
        frame_queue.put(frame_rgb)

        # Get results from the face recognition worker
        results = result_queue.get()

        for (top, right, bottom, left, name) in results:
            # Scale back up face locations since the frame was scaled down
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2
            cv2.rectangle(out_frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(out_frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

        _, buffer = cv2.imencode('.jpg', out_frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    frame_queue.put(None)
    recognition_thread.join()

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host=os.getenv("SERVER_HOST"), port=os.getenv("SERVER_PORT"), debug=False, threaded=True)
