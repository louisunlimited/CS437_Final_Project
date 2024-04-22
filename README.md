# CS437_Final_Project

Uses Flask to set up a webserver and streams raspberry pi camera feed on to `/feed`

Use `ifconfig`'s wlan0 (or equivalent) inet address to access the feed on a different device on the same network.
Then you should be able to go to your browser and connet to `http://<inet address>:5000/feed` to see the feed on a computer that's conneted to the same network as the raspberry pi.

File Structure:

```
.
├── backend
│   └── notification_service.py  # Notification Microservice
├── camera_test.py # test files for camera
├── frontend    # Frontend Admin Panel
│   ├── server.py
│   └── templates
│       └── index.html
├── haarcascade_frontalface_alt2.xml
├── kafka_test.py
├── README.md
└── server.py   # Main Server that's ran on the Raspberry Pi
```
