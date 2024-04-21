############################################
# EXAMPLE FOR combining multiple streams ###
############################################
#(might do a react/ svelte / vue/ frontend just for fun)

from flask import Flask, render_template

app = Flask(__name__)

# List of Raspberry Pi camera streams (IPs of your Raspberry Pis)
streams = [
    "http://192.168.1.13:5000/feed",
    "http://192.168.1.13:5000/feed"
]

@app.route('/')
def index():
    return render_template('index.html', streams=streams)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
