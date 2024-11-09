import pygame
from utils.config import get_display_config
import time
import math

class Display:
    def __init__(self, speedometer):
        pygame.init()
        self.display_config = get_display_config()
        self.SCREEN_WIDTH = self.display_config.get('RESOLUTION_X')
        self.SCREEN_HEIGHT = self.display_config.get('RESOLUTION_Y')
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Load gauge images
        self.gauge_bg = pygame.image.load('assets/images/gauges/speedometer/speed_gauge_bg.png')
        self.gauge_fg = pygame.image.load('assets/images/gauges/speedometer/speed_gauge.png')
        
        # Font and text properties
        self.font = pygame.font.Font(None, 36)

        # Image rectangles
        self.gauge_bg_rect = self.gauge_bg.get_rect()
        self.gauge_fg_rect = self.gauge_fg.get_rect()

        # Speedometer instance
        self.speedometer = speedometer
        
        # Speed settings
        self.MAX_SPEED = 100
        self.MAX_ANGLE = 180

        # Timing variables
        self.prev_time = 0.0

    def run(self):
        try:
            while True:
                current_time = float(time.perf_counter())
                # Calculate speed and display angle, with a default of 0 if undefined
                try:
                    speed = round(self.speedometer.calc_speed(), 1)
                except AttributeError:
                    speed = 0

                angle = -((speed / self.MAX_SPEED) * self.MAX_ANGLE)

                if current_time - self.prev_time >= 1/40:
                    self.prev_time = current_time

                    # Draw to screen
                    self.screen.fill((0, 0, 0))
                    rotated_gauge_bg = pygame.transform.rotate(self.gauge_bg, angle)
                    rotated_gauge_bg_rect = rotated_gauge_bg.get_rect(center=self.gauge_fg_rect.center)

                    self.screen.blit(rotated_gauge_bg, rotated_gauge_bg_rect)
                    self.screen.blit(self.gauge_fg, self.gauge_fg_rect)

                    # Render speed text
                    speed_text = self.font.render(f"{speed}", True, (235, 235, 235))
                    self.screen.blit(speed_text, (self.gauge_fg_rect.center))

                    pygame.display.flip()

        except KeyboardInterrupt:
            print("Display loop exited.")
