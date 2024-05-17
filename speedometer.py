import time
import math

avg_iterate = 30

prev_time = time.perf_counter()
avg_array = [0.0] * avg_iterate
counter = 0


def calc_speed(drive_ratio, tire_diameter, shaft_rpm):
    tire_circumference = math.pi * tire_diameter
    wheel_rpm = shaft_rpm / drive_ratio
    vehicle_speed = int((tire_circumference * wheel_rpm) / 1056)
    return vehicle_speed


def calc_shaft_RPM(seconds):
    rpm = 6 / seconds
    return rpm

while True:
    current_time = time.perf_counter()
    time_between = current_time - prev_time
    prev_time = current_time
    
    avg_array[counter] = calc_speed(3, 26, calc_shaft_RPM(time_between))
    counter = (counter + 1) % avg_iterate   
    
    avg = sum(avg_array) / avg_iterate
    rounded_avg = round(avg)

