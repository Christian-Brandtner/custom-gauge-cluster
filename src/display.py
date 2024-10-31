import pygame
from utils.config import get_display_config
#import gauges.speedometer as speed
import gauges.fake_speed as speed
import time
import math
pygame.init()

display_config = get_display_config()
SCREEN_WIDTH = get_display_config().get('RESOLUTION_X')
SCREEN_HEIGHT = get_display_config().get('RESOLUTION_Y')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

gauge_bg = pygame.image.load('assets/images/gauges/speedometer/speed_gauge_bg.png')
gauge_fg = pygame.image.load('assets/images/gauges/speedometer/speed_gauge.png')

gauge_bg_rect = gauge_bg.get_rect()
gauge_fg_rect = gauge_fg.get_rect()

font = pygame.font.Font(None, 36)
angle = 0

MAX_SPEED = 100
MAX_ANGLE = 180

fake_speedometer = speed.FakeSpeedometer()
try:
    while True:
        screen.fill((0, 0, 0))
        
        rotated_gauge_bg = pygame.transform.rotate(gauge_bg, angle)
        rotated_gauge_bg_rect = rotated_gauge_bg.get_rect(center=gauge_fg_rect.center)
        speed_text = font.render(f"{fake_speedometer.calc_speed()}", True, (235, 235, 235))
        speed_text = font.render(f"40", True, (235, 235, 235))
        #shaft_RPM_text = font.render(f"Shaft RPM: {int(shaft_RPM)}", True, (235, 235, 235))
        
        
        screen.blit(rotated_gauge_bg, rotated_gauge_bg_rect)
        screen.blit(gauge_fg, gauge_fg_rect)
        screen.blit(speed_text, (gauge_fg_rect.center))
        #screen.blit(shaft_RPM_text, (SCREEN_WIDTH // 8, gauge_fg_rect.centery))
        angle = -((fake_speedometer.calc_speed() / MAX_SPEED) * MAX_ANGLE)
        fake_speedometer.hall_detect()
        
        pygame.display.flip()
except KeyboardInterrupt:
    print("exit")