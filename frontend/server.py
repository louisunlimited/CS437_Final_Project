############################################
# EXAMPLE FOR combining multiple streams ###
############################################
#(might do a react/ svelte / vue/ frontend just for fun)

from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

# List of Raspberry Pi camera streams (IPs of your Raspberry Pis)
load_dotenv()
raspi_ip_addr = os.getenv('RASPI_IP')
rasapi_addresses = [raspi_ip_addr, raspi_ip_addr]
streams = [f'http://{raspi_ip_addr}:5000/feed' for raspi_ip_addr in rasapi_addresses]
webhook_endpoints = [f'http://{raspi_ip_addr}:3000/webhook' for raspi_ip_addr in rasapi_addresses]
showCameras = [True for raspi_ip_addr in rasapi_addresses]

@app.route('/')
def index():
    return render_template('index.html', streams=streams, showCameras=showCameras)

@app.route('/camera', methods=['POST'])
def button(): 
    cameraIndex = int(request.form['camera'])
    webhook_endpoint = webhook_endpoints[cameraIndex]
    if showCameras[cameraIndex]:
        requests.post(webhook_endpoint, json={'command': 'stop'})
        print('stop: camera', cameraIndex + 1)
        showCameras[cameraIndex] = False
    else:
        requests.post(webhook_endpoint, json={'command': 'start'})
        print('start: camera', cameraIndex + 1)
        showCameras[cameraIndex] = True
    print(streams)
    return render_template('index.html', streams=streams, showCameras=showCameras)

@app.route('/reboot', methods=['POST'])
def reboot():
    cameraIndex = int(request.form['camera'])
    webhook_endpoint = webhook_endpoints[cameraIndex]
    requests.post(webhook_endpoint, json={'command': 'reboot'})
    print('reboot: camera', cameraIndex + 1)
    return render_template('index.html', streams=streams, showCameras=showCameras)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
