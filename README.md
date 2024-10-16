# CS437_Final_Project

<img width="579" alt="Screenshot 2024-08-29 at 13 40 58" src="https://github.com/user-attachments/assets/3d3d8b6d-4822-423e-af88-fd3465f4989c">


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
├── louis.pickle
├── server.py   # main server
└── webhook.py  # util for controlling the server
```

## How to set up the project:
# Requirements

- Raspberry Pi 4 B
- Raspberry Pi Camera V2
    - (Optional) Cooling gadgets

# Infrastructure

## Set up GitHub SSH

```cpp
ssh-keygen -t ed25519 -C "your_email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

Then add the following catted content to your Github Account

```cpp
cat ~/.ssh/id_ed25519.pub
```

In your terminal, run 

```cpp
ssh git@github.com
```

To check if you have set up ssh keys successfully

## Python

- Should be already installed with your raspberry pi system distro

### pip3

Remove `externally-managed-environment` warning

```cpp
sudo mv /usr/lib/python3.11/EXTERNALLY-MANAGED /usr/lib/python3.11/EXTERNALLY-MANAGED.old
```

Then install the necessary dependencies 

```cpp
sudo apt-get install python3-opencv

sudo apt-get install build-essential cmake
sudo apt-get install libgtk-3-dev
sudo apt-get install libboost-all-dev

wget https://github.com/prepkg/dlib-raspberrypi/releases/latest/download/dlib_64.deb
sudo apt install -y ./dlib_64.deb
rm -rf dlib_64.deb

pip3 install face_recognition --no-deps
pip install git+https://github.com/ageitgey/face_recognition_models
```

WARNING: installing dlib from pre-compiled binary

```cpp
wget https://github.com/prepkg/dlib-raspberrypi/releases/latest/download/dlib_64.deb
sudo apt install -y ./dlib_64.deb
rm -rf dlib_64.deb
```

Is only available on 64 bit machines.

# Services

First clone the repo:

```cpp
git clone git@github.com:louisunlimited/CS437_Final_Project.git
cd CS437_Final_Project
```

Then create an `.env` file containing the following variables

```cpp
KAFKA_SERVER_URL=
KAFKA_USERNAME=
KAFKA_PASSWORD=
SERVER_HOST=
WEBHOOK_PORT=3000
SERVER_PORT=5000
```

Where 

- `SERVER_HOST` is your local ip address `wlan0:inet` , you can find this with `ifconfig` on your pi

### Server

Run

```cpp
python3 server.py
```

To start camera server

Confirm the server is working by going to `http://{rasp_ip}:{SERVER_PORT}/feed`

### Webhook

Run

```cpp
python3 webhook.py
```

Confirm the server is working by going to `http://{rasp_ip}:{WEBHOOK_PORT}`

# System

### Server Service

```cpp
sudo touch /etc/systemd/system/server.service
```

paste the following into `server.service`: CHANGE\ <USER> and <PWD> accordingly.

```
[Unit]
Description=Primary Flask Application
After=network.target

[Service]
User=<USER>
WorkingDirectory=<PWD>/CS437_Final_Project
ExecStart=/usr/bin/python3 <PWD>/server.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

Then run

```cpp
sudo systemctl enable server.service
sudo systemctl start server.service
```

to start these system services,

You can check the status with

```cpp
sudo systemctl status server.service
```

### Webhook service

Now we do the same for the webhook service

```cpp
sudo touch /etc/systemd/system/webhook.service
```

paste the following into `webhook.service`: CHANGE\ <USER> and <PWD> accordingly.

```
[Unit]
Description=Primary Flask Application
After=network.target

[Service]
User=<USER>
WorkingDirectory=<PWD>/CS437_Final_Project
ExecStart=/usr/bin/python3 <PWD>/server.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

Then run

```cpp
sudo systemctl enable webhook.service
sudo systemctl start webhook.service
```

to start these system services,

You can check the status with

```cpp
sudo systemctl status webhook.service
```

### Reboot

Now if you reboot your raspberry pi, as soon as your pi is connected to the internet, the above two service should be up as well,

You can issue a reboot like this

```cpp
sudo reboot
```

## Conclution

Congrats! Now you are all set!
