from picamera2 import Picamera2, Preview 
import cv2
import numpy as np
import time 

picam2 = Picamera2() 
camera_config = picam2.create_preview_configuration() 
picam2.configure(camera_config) 
picam2.start_preview(Preview.NULL) 
picam2.start() 
time.sleep(2) 
picam2.start_and_capture_file("image.jpg")
picam2.stop()
picam2.stop_preview()
picam2.close()