############################################
# EXAMPLE FOR combining multiple streams ###
############################################
#(might do a react/ svelte / vue/ frontend just for fun)

from flask import Flask, render_template, request, redirect, url_for
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

# List of Raspberry Pi camera streams (IPs of your Raspberry Pis)
load_dotenv()
rasapi_addresses = os.getenv('IP_LIST').split(',')
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
        res = requests.post(webhook_endpoint, json={'command': 'stop'})
        if res.ok:
            showCameras[cameraIndex] = False
    else:
        res = requests.post(webhook_endpoint, json={'command': 'start'})
        if res.ok:
            showCameras[cameraIndex] = True
    return redirect(url_for('index'))

@app.route('/reboot', methods=['POST'])
def reboot():
    cameraIndex = int(request.form['camera'])
    webhook_endpoint = webhook_endpoints[cameraIndex]
    requests.post(webhook_endpoint, json={'command': 'reboot'})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
