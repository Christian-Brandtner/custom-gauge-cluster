import time
import gauges.speedometer
# import gauges.fake_speed
import display


if __name__ == "__main__":
    speedometer = gauges.speedometer.Speedometer(speed_pin=17)
    # speedometer = gauges.fake_speed.FakeSpeedometer()
    # speedometer.run()
    display
try:
    while True:
        time.sleep(1)
        # print(speedometer.calc_speed())
        
except KeyboardInterrupt:
    
    print("\nExiting program")
finally:
    pass

