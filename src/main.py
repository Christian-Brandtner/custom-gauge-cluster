import time
import gauges.speedometer as speed
from gpiozero import DigitalInputDevice
from display import Display  # Import the Display class directly

if __name__ == "__main__":
    # Initialize speedometer and set sensor pin
    speedometer = speed.Speedometer()

    # Set up hall sensor detection
    sensor1 = DigitalInputDevice(17, pull_up=True) # set up 3 hall sensors
    sensor2 = DigitalInputDevice(18, pull_up=True)
    sensor3 = DigitalInputDevice(19, pull_up=True)
    
    sensor1.when_activated = speedometer.hall_detect(0) #updates time_between for FAST SENSOR
    
    if speedometer.sensor_time[0] > "${specified calculated mph for vehicle}":
        #if FAST SENSOR detects too low of a speed, use MED SENSOR
        #speed based on sensor_time (between_time of FAST SENSOR)
        sensor2.when_activated = speedometer.hall_detect(1) #update time_between for MED SENSOR
        # if sensor_time of MED SENSOR too slow, use FAST SENSOR
        if speedometer.sensor_time[1] > "${specified calculated mph for vehicle}":
            sensor3.when_activated = speedometer.hall_detect(2)
            
# NEED CALCULATE DIFFERENT SENSORS VALUE TO NORMALIZE
# time_between of sensor * (sensor_magnet_count / fast_sensor_magnet_count)
# fast_sensor_magnet_count = 1 && slow_sensor_magnet_count = 10 && med_sensor_magnet_count = 5
# for FAST SENSOR, fast_time_between * (10/1)
# for MED SENSOR, med_time_between * (10/5)

# ONLY WAIT FOR INTERRUPT FOR OTHER SENSORS IF GOING SLOW ENOUGH TO HANDLE THEM

    # Initialize display with speedometer instance and start it
    display = Display(speedometer)
    display.run()



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
