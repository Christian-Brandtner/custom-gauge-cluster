import time
import math
from utils.config import get_vehicle_config


class Speedometer:
    def __init__(self):
        self.vehicle_config = get_vehicle_config()
        self.TIRE_DIAMETER = self.vehicle_config.get('TIRE_DIAMETER')
        self.DRIVE_RATIO = self.vehicle_config.get('DRIVE_RATIO')
        self.INCHES_PER_MIN_TO_MPH = 1056
        self.RPM_ARRAY_COUNT = 10
        self.MAGNET_COUNT = [10, 5, 1]
        self.SENSOR_COUNT = 3
        self.TIME_COUNT = 10 # how many time values are stored for calculating rpm
        self.SENSOR_DIVIDERS = { # divide pulse time by amount of magnets on sensor. 
            0: self.MAGNET_COUNT[0],
            1: self.MAGNET_COUNT[1], 
            2: self.MAGNET_COUNT[2]
        }
        self.time_between = time.perf_counter()
        self.prev_time = time.perf_counter()
        self.rpm_array = [0.0000] * self.RPM_ARRAY_COUNT
        self.time_array = [0.0000] * (self.TIME_COUNT)
        self.sensor_time = [0.0000] * (self.SENSOR_COUNT) # store pulse time for current sensor
        self.rpm_counter = 0
        self.time_counter = 0
        self.calc_zero = True
        self.tire_circumference = math.pi * self.TIRE_DIAMETER

    def calc_shaft_rpm(self, seconds, calc_zero):
        if calc_zero:
            return 0
        else:
            rpm = 60 / seconds
            return rpm

    def calc_speed(self):
        # if self.calc_if_zero():
        #     self.time_array[self.time_counter] = 0 ## 0 time is infinite speed... ### set rpm array to 0 instead
        wheel_rpm = self.smooth_rpm() / self.DRIVE_RATIO
        speed = (self.tire_circumference * wheel_rpm) / \
            self.INCHES_PER_MIN_TO_MPH
        return speed

    def smooth_rpm(self):
        self.rpm_array[self.rpm_counter] = self.calc_shaft_rpm(
            self.time_array[self.time_counter], self.calc_if_zero())
        avg = sum(self.rpm_array) / self.RPM_ARRAY_COUNT
        rounded_avg = round(avg)
        return rounded_avg
    




    def hall_detect(self, sensor):
        # Calculate delta time (time between current and previous detection)
        self.time_between = time.perf_counter() - self.prev_time
        # Store delta time for the current sensor (used for switching logic)
        self.sensor_time[sensor] = self.time_between
        self.prev_time = time.perf_counter()  # Reset clock for the next pulse detection

        # Update counters
        # Circular buffer index for averaging RPM
        self.rpm_counter = (self.rpm_counter + 1) % self.RPM_ARRAY_COUNT
        # Fixed to store 10 time values for smoothing RPM calculation
        self.time_counter = (self.time_counter + 1) % self.TIME_COUNT

        # Store the adjusted time value (accounting for sensor's magnet count)
        self.time_array[self.time_counter] = self.time_between / \
            self.SENSOR_DIVIDERS[sensor]




    def calc_if_zero(self):
        if time.perf_counter() - self.prev_time >= 1.2 or time.perf_counter() - self.prev_time == 0:
            self.calc_zero = True
        else:
            self.calc_zero = False
        return self.calc_zero
    






    # self.time_array[self.time_counter] = self.time_between
        # if sensor(1): self.time_array[self.time_counter] = self.time_between / 5
        # time_between of sensor / (sensor_magnet_count / fast_sensor_magnet_count)

    # def run(self):
    #     self.hall_sensor.when_activated = self.hall_detect
    #     self.hall_sensor.when_activated = print("active")

# def calc_speed_time(self):
    #     speed_step = [15, 30]
    #     speed_time = [0.0000] * len(speed_step)
    #     for index, speed in enumerate(speed_step):
    #         speed_time[index] = 6 / (self.DRIVE_RATIO * (
    #             (self.INCHES_PER_MIN_TO_MPH * speed) / (math.pi * self.TIRE_DIAMETER)))
    #     return speed_time

    # def calc_seconds(self, seconds):
    #     if seconds > self.calc_speed_time()[0]:
    #         return seconds
    #     elif seconds < self.calc_speed_time()[1] and seconds >= self.calc_speed_time()[0]:
    #         seconds = sum(self.time_array[0:9:2]) / (self.MAGNET_COUNT[0] // 2)
    #     elif seconds < self.calc_speed_time()[1]:
    #         seconds = self.time_array[0]
    #     return seconds
