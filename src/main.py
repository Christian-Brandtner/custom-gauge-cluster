import time
import gauges.speedometer as speed
from gpiozero import DigitalInputDevice
from display import Display  # Import the Display class directly

if __name__ == "__main__":
    speedometer = speed.Speedometer()
    display = Display.run(speedometer)

sensor = DigitalInputDevice(17, pull_up=True)
sensor.when_activated = speedometer.hall_detect


# display = Display(speedometer)
# speedometer.run()
# speedometer.run()  # Start the speedometer data acquisition
# display.run()      # Start the display loop

# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     print("ahh")
# finally:
#     pass
