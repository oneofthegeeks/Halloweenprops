import RPi.GPIO as GPIO
import time
import concurrent.futures
import asyncio
import logging
import signal
import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', handlers=[logging.FileHandler("halloween_debug.log"), logging.StreamHandler()])

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

relay_status = {
    'bartender': False,
    'frankenstein': False,
    'werewolf': False,
    'fog': False,
    'monstermash': False
}

try:
    GPIO.setmode(GPIO.BOARD)
    relay_pins = monstermash

    # Set up all relays initially
    for pin in relay_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)  # Set all relays to OFF state initially (inactive)
        logging.debug(f"Initial setup: Set relay on pin {pin} to OFF state (HIGH)")
except Exception as e:
    logging.error(f"An error occurred during GPIO setup: {str(e)}")
    GPIO.cleanup()

# Create a thread pool executor to manage concurrent tasks
executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

def signal_handler(sig, frame):
    logging.info("Signal received, cleaning up GPIO and exiting.")
    GPIO.cleanup()
    sys.exit(0)

# Register signal handlers for graceful termination
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

@app.route("/")
def index():
    logging.info("Rendering index page.")
    return render_template('index.html', relay_durations=relay_durations, relay_status=relay_status)

@app.route("/set_fog_duration", methods=['POST'])
def set_fog_duration():
    try:
        new_duration = request.form.get('duration', type=float)
        if new_duration is not None and new_duration > 60:
            new_duration = 60
            logging.info(f"Fog duration capped at 60 seconds.")
        if new_duration is not None:
            relay_durations['fog'] = new_duration
            logging.info(f"Fog duration updated to {new_duration} seconds.")
        else:
            logging.warning("No valid duration provided for fog machine.")
        return redirect(url_for('index'))
    except Exception as e:
        logging.error(f"An error occurred while setting the fog duration: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@app.route("/<deviceName>/")
def action(deviceName):
    try:
        duration = request.args.get('duration', type=float, default=relay_durations.get(deviceName, 2))
        logging.info(f"Received request to activate {deviceName} for {duration} seconds.")
        executor.submit(asyncio.run, activate_relay(deviceName, duration))
        return jsonify({"message": f"{deviceName.capitalize()} activation started!", "status": "active"})
    except Exception as e:
        logging.error(f"An error occurred while processing the request for {deviceName}: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@app.route("/status", methods=['GET'])
def get_status():
    try:
        return jsonify(relay_status)
    except Exception as e:
        logging.error(f"An error occurred while getting relay status: {str(e)}")
        return jsonify({"message": "Could not retrieve relay status."}), 500

@app.route("/logs")
def view_logs():
    try:
        def stream_logs():
            with open("halloween_debug.log", "r") as log_file:
                for line in reversed(log_file.readlines()):
                    yield line
        return app.response_class(stream_logs(), mimetype='text/plain')
    except Exception as e:
        logging.error(f"An error occurred while trying to read the logs: {str(e)}")
        return jsonify({"message": "Could not read the log file."}), 500

@app.route("/clear_logs", methods=['POST'])
def clear_logs():
    try:
        open("halloween_debug.log", "w").close()  # Clear the log file
        logging.info("Logs have been cleared.")
        return redirect(url_for('view_logs'))
    except Exception as e:
        logging.error(f"An error occurred while trying to clear the logs: {str(e)}")
        return jsonify({"message": "Could not clear the log file."}), 500

async def activate_relay(deviceName, duration):
    try:
        logging.debug(f"Activating relay for device: {deviceName} with duration: {duration} seconds.")
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
            relay_status['monstermash'] = True
            for pin in monstermash:
                GPIO.output(pin, GPIO.LOW)  # Turn ON all relays
                logging.debug(f"Monstermash: Turned ON relay on pin {pin}")
            await asyncio.sleep(duration)  # Keep all relays on for specified duration
            for pin in monstermash:
                GPIO.output(pin, GPIO.HIGH)  # Turn OFF all relays
                logging.debug(f"Monstermash: Turned OFF relay on pin {pin}")
            relay_status['monstermash'] = False
            return

        # Activate the selected relay
        GPIO.output(relay, GPIO.LOW)  # Turn ON the relay
        relay_status[deviceName] = True
        logging.info(f"Turned ON relay for {deviceName} (pin {relay}) for {duration} seconds.")
        await asyncio.sleep(duration)  # Keep the relay on for its specified duration
        GPIO.output(relay, GPIO.HIGH)  # Turn OFF the relay
        relay_status[deviceName] = False
        logging.info(f"Turned OFF relay for {deviceName} (pin {relay}).")

    except Exception as e:
        logging.error(f"An error occurred while activating {deviceName}: {str(e)}")

if __name__ == "__main__":
    try:
        logging.info("Starting Flask application.")
        app.run(host='0.0.0.0', port=80)
    finally:
        GPIO.cleanup()  # Ensure GPIO cleanup on exit
        logging.info("Cleaned up GPIO pins on exit.")
