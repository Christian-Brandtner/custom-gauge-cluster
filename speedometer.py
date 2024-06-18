import time
import math


# DIFFERENT MAGNET NUMBERS FOR DIFFERENT SPEEDS. 1 MAGNET IS ACCURATE TO 0.1 mph @ 60MPH, 
# UNDER 30 MPH, USE 2 MAGNETS
# UNDER 15 OR 10, JUST USE 10 MAGNETS TBH. 
# PULSE COUNTER = 0, IF PULSE: COUNTER++, IF COUNTER == 10 && SPEED > 30: CALCULATE
# REASON FOR NOT USING ALL 10 AT HIGH SPEEDS IS DUE TO MAGNETS NOT BEING EXACT DISTANCES AWAY FROM EACH OTHER. THIS WOULD CAUSE NOISE
# IF TIME_BETWEEN PULSES < (0.02578 / 10MAGNETS): CALC WHEN COUNTER = 10. THIS WAY, WE USE ALL PULSES TO ESTIMATE IF SPEED IS IN RANGE, 
# BUT WE ONLY CALCULATE USING 1 MAGNET. THIS WAY, @ 10MPH WHEN DELTATIME IS 0.15469963, WE CAN GET A PULSE EVER 0.015469963
# NOW WE CAN UPDATE OUR DISPLAY @60HZ AND MEASURE SPEED AT HIGH ACCURACY
# IF WE GO 0.1 MPH, WE'D EVEN KNOW THAT AS LONG AS WE WERE DRIVING FOR AT LEAST 1.5 SECONDS.
# ALSO, IT'D BE GOOD TO FIGURE OUT HOW TO CALCULATE BASED ON HOW LONG ITS BEEN SINCE LAST PULSE WITHOUT
# NEEDING ANOTHER PULSE. 

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

