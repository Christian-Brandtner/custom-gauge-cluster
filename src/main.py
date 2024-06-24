import gauges.speedometer

if __name__ == "__main__":
    speedometer = gauges.speedometer.Speedometer(speed_pin=17)
    speedometer.run()
