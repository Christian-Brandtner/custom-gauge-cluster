import time
import RPi.GPIO as GPIO

GPIO.setmode (GPIO.BCM)

tach_pin = 17

GPIO.setup(tach_pin, GPIO.IN)

avg_iterate = 50

prev_time = time.perf_counter()
prev_state = GPIO.LOW
avg_array = [0.0] * avg_iterate
counter = 0

def calc_engine_RPM(seconds):
    rpm = 20 / seconds
    return rpm

try:
    while True:
        current_state = GPIO.input(tach_pin)
        
            
        current_time = time.perf_counter()
        time_between = current_time - prev_time
        if prev_state == GPIO.HIGH and current_state == GPIO.HIGH:
            prev_time = current_time
        
        avg_array[counter] = calc_engine_RPM(time_between)
        counter = (counter + 1) % avg_iterate
        
        avg = sum(avg_array) / avg_iterate
        rounded_avg = round(avg)
except KeyboardInterrupt:
        print("\n Exiting program")
finally:
    GPIO.cleanup()
    

    
    
