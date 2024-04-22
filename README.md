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

## How to set up the project:

Step 1: Clone the repo

```
cd ~
mkdir finalproject
cd finalproject
git clone git@github.com:louisunlimited/CS437_Final_Project.git .
```

Make sure you have a `.env` file with the following values:

```
KAFKA_SERVER_URL=
KAFKA_USERNAME=
KAFKA_PASSWORD=
SERVER_HOST=
WEBHOOK_PORT=3000
SERVER_PORT=5000
```

Step2 - Inf:

```
touch /etc/systemd/system/server.service
```

paste the following into `server.service`:
CHANGE\ <USER\> and \<PWD\> accordingly.

```
[Unit]
Description=Primary Flask Application
After=network.target

[Service]
User=<USER>
WorkingDirectory=<PWD>/finalproject
ExecStart=/usr/bin/python <PWD>/server.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

Run

```
systemctl enable server.service
systemctl start server.service
```

Create another file

```
touch /etc/systemd/system/webhook.service
```

with the following

```
[Unit]
Description=Primary Flask Application
After=network.target

[Service]
User=<USER>
WorkingDirectory=<PWD>/finalproject
ExecStart=/usr/bin/python <PWD>/webhook.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

and run

```
systemctl enable server.service
systemctl start server.service
```

Now you should be able to goto

```
<rasp-pi-IP>:5000/feed # for video feed
<rasp-pi-IP>:3000/webhook # for webhook POST endpoints
```
