import RPi.GPIO as GPIO
import time
from flask import Flask, render_template, request

app = Flask(__name__)

# Relay pin mapping
bartender = 40
frankenstein = 38
werewolf = 36
pumpkin = 32
monstermash = [40, 38, 36, 32]

GPIO.setmode(GPIO.BOARD)
relay_pins = monstermash

# Set up all relays initially
for pin in relay_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Set all relays to ON state initially

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/<deviceName>/")
def action(deviceName):
    try:
        if deviceName == 'frankenstein':
            relay = frankenstein
        elif deviceName == 'pumpkin':
            relay = pumpkin
        elif deviceName == 'werewolf':
            relay = werewolf
        elif deviceName == 'bartender':
            relay = bartender
        elif deviceName == 'monstermash':
            # Activate all relays for monstermash
            for pin in monstermash:
                GPIO.output(pin, GPIO.HIGH)  # Turn ON all relays
            time.sleep(1)  # Keep all relays on for 2 seconds
            for pin in monstermash:
                GPIO.output(pin, GPIO.LOW)  # Turn OFF all relays
            return render_template('index.html')
        else:
            return "Error: Unknown device", 404

        # Activate the selected relay
        GPIO.output(relay, GPIO.HIGH)  # Turn ON the relay
        time.sleep(2)  # Keep the relay on for 2 seconds
        GPIO.output(relay, GPIO.LOW)  # Turn OFF the relay
    except Exception as e:
        return f"An error occurred: {e}", 500
    
    return render_template('index.html')

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=80, debug=True)
    finally:
        GPIO.cleanup()  # Ensure GPIO cleanup on exit
