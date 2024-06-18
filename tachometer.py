import time
import RPi.GPIO as GPIO

IGNITION = 1 # 0 for distributor, 1 for coil on plug, 2 for drill or direct RPM with no engine


tach_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(tach_pin, GPIO.IN)

avg_iterate = 20
time_between = time.perf_counter()
prev_time = time.perf_counter()
# time_before = time.perf_counter() # for lower output without time.sleep()
prev_state = GPIO.HIGH
avg_array = [0.0000] * avg_iterate
time_array = [0.0000] * avg_iterate
counter = 0
edge_check = 0 # not needed, but extra check to avoid sensor double reading


def calc_engine_RPM(seconds, IGNITION):
    if IGNITION == 0:
        rpm = 20 / seconds
    if IGNITION == 1:
        rpm = 120 / seconds
    if IGNITION == 2:
        rpm = 60 / seconds
    return rpm

try:
    while True:
        current_state = GPIO.input(tach_pin)
        current_time = time.perf_counter()
        time_between = current_time - prev_time
        if prev_state == GPIO.HIGH and current_state == GPIO.LOW and (current_time - prev_time) >= 0.003 and edge_check == 0:
            prev_time = current_time
            # if (time_between >= (time_array[counter])): # WIP - if time between is an outlier, set to previous value to avoid spikes in RPM # basically just double reading stuff
            time_array[counter] = time_between
            prev_time = current_time
            edge_check += 1
            prev_state = 0
            print(rounded_avg)
            print("\n")
        if current_state == GPIO.HIGH:
            edge_check = 0
            prev_state = 1
            avg_array[counter] = calc_engine_RPM(time_between, IGNITION)
            counter = (counter + 1) % avg_iterate
            avg = sum(avg_array) / avg_iterate
            rounded_avg = round(avg)
            # if current_time - time_before >= 0.0161616: # for 60fps output
            #     time_before = current_time
except KeyboardInterrupt:
    print("\n Exiting program")
finally:
    GPIO.cleanup()
