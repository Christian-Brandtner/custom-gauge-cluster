import time
import math

avg_iterate = 30

prev_time = time.perf_counter()
avg_array = [0.0] * avg_iterate
counter = 0
time_before = time.perf_counter()

per_second = 120

def calc_speed(drive_ratio, tire_diameter, shaft_rpm):
    tire_circumference = math.pi * tire_diameter
    wheel_rpm = shaft_rpm / drive_ratio
    vehicle_speed = (tire_circumference * wheel_rpm) / 1056
    return vehicle_speed


def calc_shaft_RPM(seconds):
    rpm = 30 / seconds
    return rpm

while True:
    sec = 1 / per_second
    current_time = time.perf_counter()
    per_second += 0.00000005
    if current_time - time_before >= 1/22: # for 60fps output
        time_before = current_time
        print(calc_speed(3, 26, calc_shaft_RPM(sec)))
        