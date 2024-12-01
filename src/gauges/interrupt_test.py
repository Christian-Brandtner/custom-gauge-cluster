import time
import math


# Stub function to mimic getting vehicle configuration
def get_vehicle_config():
    return {
        'TIRE_DIAMETER': 30,  # Example value in inches
        'DRIVE_RATIO': 3.55  # Example value
    }


class Speedometer:
    def __init__(self):
        self.vehicle_config = get_vehicle_config()
        self.TIRE_DIAMETER = self.vehicle_config.get('TIRE_DIAMETER')
        self.DRIVE_RATIO = self.vehicle_config.get('DRIVE_RATIO')
        self.INCHES_PER_MIN_TO_MPH = 1056
        self.RPM_ARRAY_COUNT = 10
        self.MAGNET_COUNT = [10, 5, 1]
        self.SENSOR_COUNT = 3
        self.TIME_COUNT = 10  # How many time values are stored for calculating RPM
        self.SENSOR_DIVIDERS = {  # Divide pulse time by the number of magnets on the sensor
            0: self.MAGNET_COUNT[0],
            1: self.MAGNET_COUNT[1],
            2: self.MAGNET_COUNT[2]
        }
        self.time_between = 0.0
        self.prev_time = time.perf_counter()
        self.rpm_array = [0.0] * self.RPM_ARRAY_COUNT
        self.time_array = [0.0] * self.TIME_COUNT
        # Store pulse time for current sensor
        self.sensor_time = [0.0] * self.SENSOR_COUNT
        self.rpm_counter = 0
        self.time_counter = 0
        self.calc_zero = True
        self.tire_circumference = math.pi * self.TIRE_DIAMETER

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


# Test harness
if __name__ == "__main__":
    speedometer = Speedometer()

    # Simulate calling hall_detect and measure execution time
    sensor = 0  # Testing with the first sensor (0)
    iterations = 1000  # Number of test iterations

    start_time = time.perf_counter()
    for _ in range(iterations):
        speedometer.hall_detect(sensor)
    end_time = time.perf_counter()

    total_time = (end_time - start_time) * 1e6  # Convert to microseconds
    avg_time = total_time / iterations

    print(f"Total execution time for {iterations} calls: {total_time:.2f} µs")
    print(f"Average execution time per call: {avg_time:.2f} µs")
