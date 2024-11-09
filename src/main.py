import time
import gauges.speedometer as speed
#from display import Display  # Import the Display class directly

if __name__ == "__main__":
    speedometer = speed.Speedometer(speed_pin=17)
    #display = Display(speedometer)
    
    #speedometer.run()  # Start the speedometer data acquisition
    #display.run()      # Start the display loop
    
while True:
    try:
        time.sleep(1/60)
        speedometer.run()
    except: print("bye")
