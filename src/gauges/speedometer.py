import time
from gpiozero import DigitalInputDevice

speed_pin = 17


# UPDATE TO USE CLASS
# ALSO, REMOVE ALL COMMENTS, ADD SPEED LEVEL FUNCTIONALITY, AND EXPERIMENT WITH bounce_time, USE EXPONENTIAL SMOOTHING


# Set up the pin with internal pull-up resistor
hall_sensor = DigitalInputDevice(speed_pin, pull_up=True, bounce_time=0.001)

AVERAGE_ITERATE = 20

time_between = time.perf_counter()
prev_time = time.perf_counter()

avg_array = [0.0000] * AVERAGE_ITERATE
time_array = [0.0000] * AVERAGE_ITERATE

counter = 0
edge_check = 0
prev_state = 1  # Initial value for prev_state

def calc_speed(seconds):
    if seconds == 0 or seconds > 2:
        return 0
    else:
        rpm = 60 / seconds
        return rpm

def smooth_speed():
    global counter, avg_array, time_between
    avg_array[counter] = calc_speed(time_between)
    avg = sum(avg_array) / AVERAGE_ITERATE
    rounded_avg = round(avg)
    return rounded_avg

def hall_detect():
    global prev_time, prev_state, edge_check, counter, time_between
    time_between = time.perf_counter() - prev_time
    prev_time = time.perf_counter()
    counter = (counter + 1) % AVERAGE_ITERATE
    

hall_sensor.when_activated = hall_detect

try:
    while True:
        time.sleep(1/60)
        print(smooth_speed())
except KeyboardInterrupt:
    print("\nExiting program")
finally:
    pass  # gpiozero handles cleanup automatically
