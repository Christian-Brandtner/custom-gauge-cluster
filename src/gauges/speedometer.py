import time
from gpiozero import DigitalInputDevice

speed_pin = 17


# UPDATE TO USE CLASS
# ALSO, REMOVE ALL COMMENTS, ADD SPEED LEVEL FUNCTIONALITY, AND EXPERIMENT WITH bounce_time, USE EXPONENTIAL SMOOTHING

# CREATE FUNCTION TO CALCULATE TIME_BETWEEN AT < 15, < 30 AND > 30 MPH. DONE AT STARTUP, BASED ON CONFIGS LIKE TIRE SIZE, DRIVE RATIO ETC. 


hall_sensor = DigitalInputDevice(speed_pin, pull_up=True, bounce_time=0.001)

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

def calc_seconds(seconds):
    if seconds > 0.00835:
        return seconds
    elif seconds < 0.00835 and seconds > 0.004147:
        seconds = sum(time_array[0:9:2]) / 5
    elif seconds < 0.004147:
        seconds = time_array[0]
    return seconds

def calc_speed(seconds):
    if seconds == 0 or seconds > 1.2:
        return 0
    else:
        speed = 60 / seconds
        return speed

def smooth_speed():
    global avg_counter, avg_array, time_between
    avg_array[avg_counter] = calc_speed(calc_seconds(time_array))
    avg = sum(avg_array) / AVERAGE_ITERATE
    rounded_avg = round(avg)
    return rounded_avg

def hall_detect():
    global prev_time, avg_counter, time_between
    time_between = time.perf_avg_counter() - prev_time
    prev_time = time.perf_avg_counter()
    avg_counter = (avg_counter + 1) % AVERAGE_ITERATE
    time_counter = (time_counter + 1) % MAGNET_COUNT
    time_array[time_counter] = time_between
    
hall_sensor.when_activated = hall_detect

try:
    while True:
        time.sleep(1/60)
        print(smooth_speed())
except KeyboardInterrupt:
    print("\nExiting program")
finally:
    pass
