import time
import RPi.GPIO as GPIO

# GPIO setup
OUTPUT_PIN = 17
INPUT_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(OUTPUT_PIN, GPIO.OUT)
GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Timing variables
interrupt_times = []
test_iterations = 1000


def interrupt_handler(channel):
    global start_time
    interrupt_times.append(time.perf_counter() - start_time)


# Attach the interrupt
GPIO.add_event_detect(INPUT_PIN, GPIO.RISING, callback=interrupt_handler)

print(f"Running {test_iterations} iterations...")
for _ in range(test_iterations):
    start_time = time.perf_counter()
    GPIO.output(OUTPUT_PIN, GPIO.HIGH)  # Set output high
    GPIO.output(OUTPUT_PIN, GPIO.LOW)   # Set output low
    time.sleep(0.001)  # Allow some time for interrupts to process

# Calculate results
if interrupt_times:
    avg_time = sum(interrupt_times) / len(interrupt_times) * \
        1e6  # Convert to microseconds
    print(f"Average interrupt latency: {avg_time:.2f} µs")
else:
    print("No interrupts detected!")

# Cleanup
GPIO.cleanup()
