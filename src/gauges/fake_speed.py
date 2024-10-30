import time
import math
# from utils.config import get_vehicle_config
# from gpiozero import DigitalInputDevice

speed = 0
direction = 'up'

def direct_value():
    global speed
    global direction
    if direction == 'up' and speed <= 99.6:
        speed += 0.4
    elif direction == 'down' and speed >= 0.8:
        speed -= 0.8
    if speed >= 99.6:
        direction = 'down'
    if speed <= 0.8 and direction == 'down':
        direction = 'up'
    round(speed, 2)
    return speed

# while True:
#     time.sleep(1/60)
#     print(direct_value())