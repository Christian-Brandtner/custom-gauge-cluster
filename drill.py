import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
tach_pin = 17
GPIO.setup(tach_pin, GPIO.IN)
avg_iterate = 20
time_between = time.perf_counter()
prev_time = time.perf_counter()
prev_state = GPIO.HIGH
avg_array = [0.0000] * avg_iterate
time_array = [0.0000] * avg_iterate
counter = 0
one_count = 0
time_before = time.perf_counter()

def calc_engine_RPM(seconds):
    rpm = 60 / seconds
    return rpm

try:
    while True:
        current_state = GPIO.input(tach_pin)
        current_time = time.perf_counter()
        time_between = current_time - prev_time
        if prev_state == GPIO.HIGH and current_state == GPIO.LOW and (current_time - prev_time) >= 0.005 and one_count == 0:
            prev_time = current_time
            time_array[counter] = time_between
            prev_time = current_time
            one_count += 1
            prev_state = 0
            print(rounded_avg)
            print("\n")
        if current_state == GPIO.HIGH:
            one_count = 0
            prev_state = 1
            avg_array[counter] = calc_engine_RPM(time_between)
            counter = (counter + 1) % avg_iterate
            avg = sum(avg_array) / avg_iterate
            rounded_avg = round(avg)
            # if current_time - time_before >= 0.0161616: # for 60fps output
            #     time_before = current_time 
except KeyboardInterrupt:
    print("\n Exiting program")
finally:
    GPIO.cleanup()
