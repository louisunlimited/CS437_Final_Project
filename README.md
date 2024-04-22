# CS437_Final_Project

Uses Flask to set up a webserver and streams raspberry pi camera feed on to `/feed`

Use `ifconfig`'s wlan0 (or equivalent) inet address to access the feed on a different device on the same network.
Then you should be able to go to your browser and connet to `http://<inet address>:5000/feed` to see the feed on a computer that's conneted to the same network as the raspberry pi.

App password in mailsender.py file, SMTP may fail if this is not the right app passsword. Need to generate an app password for each new device.