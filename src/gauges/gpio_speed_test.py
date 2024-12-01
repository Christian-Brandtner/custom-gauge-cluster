import time
from gpiozero import LED, DigitalInputDevice

# GPIO pin setup
output_pin = 17  # Output pin
input_pin = 18   # Input pin

# Configure the pins
led = LED(output_pin)
sensor = DigitalInputDevice(input_pin, pull_up=True)

# Timing variables
interrupt_times = []
test_iterations = 1000

# Interrupt callback


def interrupt_handler():
    global interrupt_start
    interrupt_times.append(time.perf_counter() - interrupt_start)


# Attach the interrupt
sensor.when_activated = interrupt_handler

# Run the test
print(f"Running {test_iterations} iterations...")
for _ in range(test_iterations):
    interrupt_start = time.perf_counter()
    led.on()  # Trigger the output pin
    time.sleep(0.00001)  # Ensure pulse is long enough to detect
    led.off()  # Turn off the output pin
    time.sleep(0.001)  # Short delay between pulses

# Calculate and display results
if interrupt_times:
    avg_time = sum(interrupt_times) / len(interrupt_times) * \
        1e6  # Convert to microseconds
    print(f"Average interrupt latency: {avg_time:.2f} µs")
else:
    print("No interrupts detected!")

# Cleanup
sensor.close()
led.close()
