import time
import gauges.speedometer as speed
from gpiozero import DigitalInputDevice
from display import Display  # Import the Display class directly

if __name__ == "__main__":
    # Initialize speedometer and set sensor pin
    speedometer = speed.Speedometer()

    # Set up hall sensor detection
    def sensor(pin, magnet_count): 
        sensor = [DigitalInputDevice(pin, pull_up=True), magnet_count]
        return sensor
    
    sensors = [sensor(17, speedometer.MAGNET_COUNT[0]), sensor(18, speedometer.MAGNET_COUNT[1]), sensor(19, speedometer.MAGNET_COUNT[2])] # set up 3 hall sensors
    
    sensors[0].when_activated = lambda: speedometer.hall_detect(0) #updates time_between for FAST SENSOR
    
    if speedometer.sensor_time[0] > "${specified calculated mph for vehicle}":
        #if FAST SENSOR detects too low of a speed, use MED SENSOR
        #speed based on sensor_time (between_time of FAST SENSOR)
        sensors[1].when_activated = lambda: speedometer.hall_detect(1) #update time_between for MED SENSOR
        # if sensor_time of MED SENSOR too slow, use FAST SENSOR
        if speedometer.sensor_time[1] > "${specified calculated mph for vehicle}":
            sensors[2].when_activated = lambda: speedometer.hall_detect(2)
            
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
