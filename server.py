from flask import Flask, Response
import picamera2
import cv2

app = Flask("123")
camera = picamera2.Picamera2()
camera_config = camera.create_preview_configuration()
camera.configure(camera_config)
camera.start_preview(picamera2.Preview.NULL)
camera.start()

def generate_frames():
    while True:
        buffer = camera.capture_array()
        buffer = cv2.cvtColor(buffer, cv2.COLOR_BGR2RGB)
        _, buffer = cv2.imencode('.jpg', buffer)
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
    

# host: inet address of the server (example: wlan0 -> inet)
if __name__ == "__main__":
    app.run(host="192.168.1.13", port=5000, debug=False, threaded=True)