import pygame
import sys
import math

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

DRIVE_RATIO = 3
TIRE_DIAMETER = 26

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Digital Gauge Cluster 0.1.0-alpha")

res_image1 = pygame.image.load('./images/custom_bg.png')
res_image2 = pygame.image.load('./images/custom_fg.png')

res_image_rect1 = res_image1.get_rect()
res_image_rect2 = res_image2.get_rect()

res_image_rect1.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
res_image_rect2.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

denominator = 1

seconds = 1/denominator

    
    
def calc_needle_rotation(max_rotation, min_value, max_value, value):
    rotation = (value / max_value) * max_rotation
    return rotation

def calc_speed(drive_ratio, tire_diameter, shaft_rpm):
    tire_circumference = math.pi * tire_diameter
    wheel_rpm = shaft_rpm / drive_ratio
    vehicle_speed = int((tire_circumference * wheel_rpm) / 1056)
    return vehicle_speed

def calc_shaft_RPM(seconds):
    rpm = 6 / seconds
    return rpm

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0))
    rotated_gauge_bg = pygame.transform.rotate(res_image1, calc_needle_rotation(180, 0, 100, calc_speed(3, 26, calc_shaft_RPM(0.00161)))*-1)
    rotated_gauge_bg_rect = rotated_gauge_bg.get_rect(center=res_image_rect1.center)
    screen.blit(rotated_gauge_bg, rotated_gauge_bg_rect)
    screen.blit(res_image2, res_image_rect2)
    pygame.display.flip()
    print(calc_speed(DRIVE_RATIO, TIRE_DIAMETER, calc_shaft_RPM(0.0016)))
    denominator += 0.05