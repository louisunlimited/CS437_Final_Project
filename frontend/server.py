############################################
# EXAMPLE FOR combining multiple streams ###
############################################
#(might do a react/ svelte / vue/ frontend just for fun)

from flask import Flask, render_template
import os

app = Flask(__name__)

# List of Raspberry Pi camera streams (IPs of your Raspberry Pis)
raspi_ip_addr = os.getenv('RASPI_IP')
streams = [
    f"http://{raspi_ip_addr}:5000/feed",
    f"http://{raspi_ip_addr}:5000/feed"
]

@app.route('/')
def index():
    return render_template('index.html', streams=streams)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
