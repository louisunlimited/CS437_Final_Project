from flask import Flask, request
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask("Webhook")

@app.route('/')
def home():
    return "Hello, this is the webhook Flask app running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Assuming JSON payload
    if 'command' in data:
        if data['command'] == 'start':
            subprocess.run(['sudo', 'systemctl', 'start', 'server.service'])
            return "Starting Flask application", 200
        elif data['command'] == 'stop':
            subprocess.run(['sudo', 'systemctl', 'stop', 'server.service'])
            return "Stopping Flask application", 200
        elif data['command'] == 'reboot':
            subprocess.run(['sudo', 'reboot'])
            return "Rebooting Entire Server, please wait for a while", 200
    return "Invalid command", 400

if __name__ == '__main__':
    app.run(host=os.getenv("SERVER_HOST"), port=os.getenv("WEBHOOK_PORT"))
