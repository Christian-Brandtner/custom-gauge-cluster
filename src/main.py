import time
import gauges.speedometer


if __name__ == "__main__":
    speedometer = gauges.speedometer.Speedometer(speed_pin=17)
    speedometer.run()
    
try:
    while True:
        time.sleep(1 / 60)
        print(speedometer.calc_speed())
except KeyboardInterrupt:
    print("\nExiting program")
finally:
    pass

