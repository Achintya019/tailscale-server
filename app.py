import subprocess
import datetime
import time
import threading
import json
from flask import Flask, render_template

app = Flask(__name__)

# File path for saving and loading device statuses
STATUS_FILE = 'device_statuses.json'

# Sample data for initial devices (you can replace this with your actual data handling logic)
devices = [
    {'hostname': 'cpu-57-masterpc', 'addresses': ['100.122.28.15'], 'os_version': '1.56.1 / Linux 5.15.0-107-generic', 'last_seen': 'disconnected', 'first_unable_to_ping': None},
    {'hostname': 'eagam', 'addresses': ['100.70.242.110'], 'os_version': '1.46.1 / Linux 5.15.0-107-generic', 'last_seen': 'disconnected', 'first_unable_to_ping': None},
    {'hostname': 'euler-vin', 'addresses': ['100.86.164.86'], 'os_version': '1.60.1 / Linux 5.15.0-107-generic', 'last_seen': 'disconnected', 'first_unable_to_ping': None},
    {'hostname': 'frodobaggins', 'addresses': ['100.117.242.125'], 'os_version': '1.66.4/Linux 5.15.0-113-generic', 'last_seen': 'disconnected', 'first_unable_to_ping': None},
    {'hostname': 'huawei-stk-l22', 'addresses': ['100.119.123.97'], 'os_version': '1.60.1/Android 10', 'last_seen': 'disconnected', 'first_unable_to_ping': None},
    {'hostname': 'l-583-pdi', 'addresses': ['100.121.81.93'], 'os_version': '1.66.1/Linux (6.5.0-41-generic)', 'last_seen': 'disconnected', 'first_unable_to_ping': None},
    {'hostname': 'l218-achintya-eag', 'addresses': ['100.119.26.61'], 'os_version': '1.68.1/Linux (5.15.0-113-generic)', 'last_seen': 'disconnected', 'first_unable_to_ping': None},
    {'hostname': 'machine', 'addresses': ['100.80.23.38'], 'os_version': '1.68.1/Linux 5.15.0-113-generic', 'last_seen': 'disconnected', 'first_unable_to_ping': None},
    {'hostname': 'nvidia-batteryline-topdown', 'addresses': ['100.109.233.33'], 'os_version': '1.64.0/Linux 4.9.253-tegra', 'last_seen': 'disconnected', 'first_unable_to_ping': None},
    {'hostname': 'qualcomm-msm8953-for-arm64', 'addresses': ['100.69.8.4'], 'os_version': '1.52.0/Android 10', 'last_seen': 'disconnected', 'first_unable_to_ping': None},
    {'hostname': 'thermalcam-username-l-146', 'addresses': ['100.72.170.98'], 'os_version': '1.66.1/Linux 6.5.0-41-generic', 'last_seen': 'disconnected', 'first_unable_to_ping': None}
]

def save_status_to_file():
    with open(STATUS_FILE, 'w') as file:
        json.dump(devices, file, indent=4)

def load_status_from_file():
    try:
        with open(STATUS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None

@app.route('/')
def index():
    error = None  # You can add error handling logic here
    return render_template('index1.html', devices=devices, error=error)

def ping_all():
    while True:
        try:
            for device in devices:
                ip = device['addresses'][0]
                ping_response = subprocess.run(['ping', ip, '-c', '4'], capture_output=True, text=True)
                if ping_response.returncode == 0:
                    device['last_seen'] = 'connected'  # Reset last seen on successful ping
                    device['first_unable_to_ping'] = None
                else:
                    if device['first_unable_to_ping'] is None:
                        device['first_unable_to_ping'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    device['last_seen'] = device['first_unable_to_ping']
            print("All devices pinged and statuses updated.")
            save_status_to_file()  # Save statuses to file after updating
        except Exception as e:
            print(f"Error during ping all: {e}")
        time.sleep(10)

def start_ping_thread():
    ping_thread = threading.Thread(target=ping_all)
    ping_thread.daemon = True
    ping_thread.start()

if __name__ == '__main__':
    # Load statuses from file if available
    loaded_devices = load_status_from_file()
    if loaded_devices:
        devices = loaded_devices
    
    start_ping_thread()
    
    # Start the Flask app
    try:
        app.run(debug=True)
    except (KeyboardInterrupt, SystemExit):
        print("Shutting down the app...")
