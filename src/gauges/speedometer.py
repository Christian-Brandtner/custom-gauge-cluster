import time
import math
from utils.config import get_vehicle_config
from gpiozero import DigitalInputDevice

speed_pin = 17


# UPDATE TO USE CLASS
# EXPERIMENT WITH bounce_time, USE EXPONENTIAL SMOOTHING



hall_sensor = DigitalInputDevice(speed_pin, pull_up=True, bounce_time=0.001)
vehicle_config = get_vehicle_config()

TIRE_DIAMETER = vehicle_config.get('TIRE_DIAMETER')
DRIVE_RATIO = vehicle_config.get('DRIVE_RATIO')

INCHES_PER_MIN_TO_MPH = 1056
AVERAGE_ITERATE = 20
MAGNET_COUNT = 10

time_between = time.perf_avg_counter()
prev_time = time.perf_avg_counter()

avg_array = [0.0000] * AVERAGE_ITERATE
time_array = [0.0000] * (MAGNET_COUNT-1)

time_counter = 0
avg_counter = 0
edge_check = 0
prev_state = 1

def calc_speed_time():
    speed_step = [15, 30]
    speed_time = [0] * len(speed_step)
    for index, speed in enumerate(speed_step):
        speed_time[index] = 6 / (DRIVE_RATIO * ((INCHES_PER_MIN_TO_MPH * speed) / (math.pi * TIRE_DIAMETER)))
    return speed_time

def calc_seconds(seconds):
    if seconds > calc_speed_time()[0]:
        return seconds
    elif seconds < calc_speed_time()[1] and seconds >= calc_speed_time()[0]:
        seconds = sum(time_array[0:9:2]) / (MAGNET_COUNT//2)
    elif seconds < calc_speed_time()[1]:
        seconds = time_array[0]
    return seconds

def calc_shaft_rpm(seconds):
    if seconds == 0 or seconds > 1.2:
        return 0
    else:
        rpm = 60 / seconds
        return rpm
    
def calc_speed():
    tire_circumference = math.pi*TIRE_DIAMETER
    wheel_rpm = smooth_rpm() / DRIVE_RATIO
    speed = (tire_circumference*wheel_rpm)/INCHES_PER_MIN_TO_MPH
    return speed

def smooth_rpm():
    global avg_counter, avg_array, time_between
    avg_array[avg_counter] = calc_shaft_rpm(calc_seconds(time_array))
    avg = sum(avg_array) / AVERAGE_ITERATE
    rounded_avg = round(avg)
    return rounded_avg

def hall_detect(): # update when sensor activated
    global prev_time, avg_counter, time_between, time_counter
    time_between = time.perf_avg_counter() - prev_time
    prev_time = time.perf_avg_counter()
    avg_counter = (avg_counter + 1) % AVERAGE_ITERATE
    time_counter = (time_counter + 1) % MAGNET_COUNT
    time_array[time_counter] = time_between
    
hall_sensor.when_activated = hall_detect

try:
    while True:
        time.sleep(1/60)
        print(calc_speed())
except KeyboardInterrupt:
    print("\nExiting program")
finally:
    pass
