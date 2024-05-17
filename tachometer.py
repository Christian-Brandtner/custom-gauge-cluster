import time

avg_iterate = 3000

prev_time = time.perf_counter()
avg_array = [0.0] * avg_iterate
counter = 0

def calc_engine_RPM(seconds):
    rpm = 20 / seconds
    return rpm

while True:
    current_time = time.perf_counter()
    time_between = current_time - prev_time
    prev_time = current_time
    
    avg_array[counter] = calc_engine_RPM(time_between)
    counter = (counter + 1) % avg_iterate
    
    avg = sum(avg_array) / avg_iterate
    rounded_avg = round(avg)
