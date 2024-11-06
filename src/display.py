import pygame
from utils.config import get_display_config
# import gauges.speedometer as speed
import gauges.speedometer as speed
import time
import math
pygame.init()

display_config = get_display_config()
SCREEN_WIDTH = get_display_config().get('RESOLUTION_X')
SCREEN_HEIGHT = get_display_config().get('RESOLUTION_Y')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

gauge_bg = pygame.image.load(
    'assets/images/gauges/speedometer/speed_gauge_bg.png')
gauge_fg = pygame.image.load(
    'assets/images/gauges/speedometer/speed_gauge.png')

gauge_bg_rect = gauge_bg.get_rect()
gauge_fg_rect = gauge_fg.get_rect()

font = pygame.font.Font(None, 36)
angle = 0

MAX_SPEED = 100
MAX_ANGLE = 180

prev_time = 0.0
current_time = 0.0
between_time = 0.0

display_speed = 0.0


def update_display():
    screen.fill((0, 0, 0))

    speed_text = font.render(
        f"{round(display_speed, 1)}", True, (235, 235, 235))
    angle = -((round(display_speed, 4) / MAX_SPEED) * MAX_ANGLE)

    rotated_gauge_bg = pygame.transform.rotate(gauge_bg, angle)
    rotated_gauge_bg_rect = rotated_gauge_bg.get_rect(
        center=gauge_fg_rect.center)

    screen.blit(rotated_gauge_bg, rotated_gauge_bg_rect)
    screen.blit(gauge_fg, gauge_fg_rect)
    screen.blit(speed_text, (gauge_fg_rect.center))
    # screen.blit(shaft_RPM_text, (SCREEN_WIDTH // 8, gauge_fg_rect.centery))

    pygame.display.flip()


count = 0
speedometer = speed.Speedometer()
try:
    while True:
        current_time = float(time.perf_counter())
        display_speed = speedometer.calc_speed()
        if float(current_time - prev_time) >= (1/30):
            count += 1
            update_display()

            prev_time = current_time

except KeyboardInterrupt:
    print("exit")
