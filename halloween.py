import RPi.GPIO as GPIO
import time
import threading
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Relay activation durations in seconds
relay_durations = {
    'bartender': 2,
    'frankenstein': 3,
    'werewolf': 4,
    'fog': 5,
    'monstermash': 1  # Duration for individual relays when activating all in monstermash
}

# Relay pin mapping
bartender = 40
frankenstein = 38
werewolf = 36
fog = 32
monstermash = [40, 38, 36, 32]

GPIO.setmode(GPIO.BOARD)
relay_pins = monstermash

# Set up all relays initially
for pin in relay_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # Set all relays to OFF state initially (inactive)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/<deviceName>/")
def action(deviceName):
    try:
        # Return an immediate response to confirm the request
        response = jsonify({"message": f"{deviceName.capitalize()} activation started!"})
        
        # Start a new thread to handle the GPIO actions
        thread = threading.Thread(target=activate_relay, args=(deviceName,))
        thread.start()

        return response
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

def activate_relay(deviceName):
    try:
        if deviceName == 'frankenstein':
            relay = frankenstein
        elif deviceName == 'fog':
            relay = fog
        elif deviceName == 'werewolf':
            relay = werewolf
        elif deviceName == 'bartender':
            relay = bartender
        elif deviceName == 'monstermash':
            # Activate all relays for monstermash
            for pin in monstermash:
                GPIO.output(pin, GPIO.LOW)  # Turn ON all relays
            time.sleep(relay_durations.get('monstermash', 1))  # Keep all relays on for specified duration
            for pin in monstermash:
                GPIO.output(pin, GPIO.HIGH)  # Turn OFF all relays
            return

        # Activate the selected relay
        GPIO.output(relay, GPIO.LOW)  # Turn ON the relay
        time.sleep(relay_durations.get(deviceName, 2))  # Keep the relay on for its specified duration
        GPIO.output(relay, GPIO.HIGH)  # Turn OFF the relay

    except Exception as e:
        print(f"An error occurred while activating {deviceName}: {str(e)}")

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=80)
    finally:
        GPIO.cleanup()  # Ensure GPIO cleanup on exit
