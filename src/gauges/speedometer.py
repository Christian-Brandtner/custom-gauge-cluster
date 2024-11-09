import time
import math
from utils.config import get_vehicle_config
from gpiozero import DigitalInputDevice

class Speedometer:
    def __init__(self, speed_pin):
        self.speed_pin = speed_pin
        self.hall_sensor = DigitalInputDevice(
            self.speed_pin, pull_up=True, bounce_time=0.001)
        self.vehicle_config = get_vehicle_config()  
        self.TIRE_DIAMETER = self.vehicle_config.get('TIRE_DIAMETER')
        self.DRIVE_RATIO = self.vehicle_config.get('DRIVE_RATIO')
        self.INCHES_PER_MIN_TO_MPH = 1056
        self.AVERAGE_ITERATE = 50
        self.MAGNET_COUNT = 10
        self.time_between = time.perf_counter()
        self.prev_time = time.perf_counter()
        self.avg_array = [0.0000] * self.AVERAGE_ITERATE
        self.time_array = [0.0000] * (self.MAGNET_COUNT)
        self.avg_counter = 0
        self.time_counter = 0

    def calc_speed_time(self):
        speed_step = [15, 30]
        speed_time = [0.0000] * len(speed_step)
        for index, speed in enumerate(speed_step):
            speed_time[index] = 6 / (self.DRIVE_RATIO * (
                (self.INCHES_PER_MIN_TO_MPH * speed) / (math.pi * self.TIRE_DIAMETER)))
        return speed_time

    def calc_seconds(self, seconds):
        if seconds > self.calc_speed_time()[0]:
            return seconds
        elif seconds < self.calc_speed_time()[1] and seconds >= self.calc_speed_time()[0]:
            seconds = sum(self.time_array[0:9:2]) / (self.MAGNET_COUNT // 2)
        elif seconds < self.calc_speed_time()[1]:
            seconds = self.time_array[0]
        return seconds

    def calc_shaft_rpm(self, seconds):
        if seconds == 0 or seconds > 1.2:
            return 0
        else:
            rpm = 60 / seconds
            return rpm

    def calc_speed(self):
        tire_circumference = math.pi * self.TIRE_DIAMETER
        wheel_rpm = self.smooth_rpm() / self.DRIVE_RATIO
        speed = (tire_circumference * wheel_rpm) / self.INCHES_PER_MIN_TO_MPH
        return speed

    def smooth_rpm(self):
        self.avg_array[self.avg_counter] = self.calc_shaft_rpm(
            self.calc_seconds(self.time_array[self.time_counter]))
        avg = sum(self.avg_array) / self.AVERAGE_ITERATE
        rounded_avg = round(avg)
        return rounded_avg

    def hall_detect(self):
        self.time_between = time.perf_counter() - self.prev_time
        self.prev_time = time.perf_counter()
        self.avg_counter = (self.avg_counter + 1) % self.AVERAGE_ITERATE
        self.time_counter = (self.time_counter + 1) % self.MAGNET_COUNT
        self.time_array[self.time_counter] = self.time_between

    def run(self):
        self.hall_sensor.when_activated = self.hall_detect
        self.hall_sensor.when_activated = print("active")
