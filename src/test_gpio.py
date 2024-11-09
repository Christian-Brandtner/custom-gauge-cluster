from gpiozero import DigitalInputDevice
import time

sensor = DigitalInputDevice(17, pull_up=True)

def hall_detect():
    print("Hall sensor triggered")

sensor.when_activated = hall_detect

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
