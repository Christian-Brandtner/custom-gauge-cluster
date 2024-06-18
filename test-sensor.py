import RPi.GPIO as GPIO
import time

# Use BCM pin numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin
SENSOR_PIN = 17

# Set up the GPIO pin as an input
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def sensor_callback(channel):
    print("Magnet detected")

# Add edge detection on the sensor pin
try:
    GPIO.add_event_detect(SENSOR_PIN, GPIO.FALLING, callback=sensor_callback)
except RuntimeError as e:
    print(f"Runtime error: {e}")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting program")

# Clean up GPIO settings
GPIO.cleanup()
