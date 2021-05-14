# -*- coding: utf-8 -*-
"""
Created on Fri May  7 21:43:50 2021

@author: Korean_Crimson
"""

import math
import time
import pygame

pygame.init()
SCREEN = pygame.display.set_mode((600, 400))
MOUSE_POS = pygame.mouse.get_pos()
TERMINATED = False
DELAY = 0.02
LAST_TIME = time.time()
RECT = pygame.Rect(200, 200, 200, 200)
RECT2 = pygame.Rect(100, 0, 50, 400)
LIGHTSOURCES = [(300, 300), (0, 0)]
LIGHTINTENSITY = 0
LIGHTCOLOUR = (255, 255, 153, 100)

def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def draw_lighting():
    #sides of the black square
    midpoints_x = [(300, 200), (300, 400)]
    midpoints_y = [(200, 300), (400, 300)]
    vertices = [(200, 200), (200, 400), (400, 200), (400, 400)]

    for light_source in LIGHTSOURCES:
        x, y = light_source
        #x side
        _, min_x = min([(distance(light_source, point), point) for point in midpoints_x], key=lambda x: x[0])
        xdistances = [distance(min_x, v) for v in vertices]
        xpoints, _ = zip(*sorted(zip(vertices, xdistances), key=lambda x: x[1]))
        points = [light_source, *xpoints[:2]]

        surf = pygame.Surface(SCREEN.get_size(), pygame.SRCALPHA)
        pygame.draw.polygon(surf, LIGHTCOLOUR, points)
        y1, y2 = 200, 400
        if not y1 < y < y2:
            SCREEN.blit(surf, (0, 0))

        #y side
        _, min_y = min([(distance(light_source, point), point) for point in midpoints_y], key=lambda x: x[0])
        ydistances = [distance(min_y, v) for v in vertices]
        ypoints, _ = zip(*sorted(zip(vertices, ydistances), key=lambda x: x[1]))
        points = [light_source, *ypoints[:2]]

        surf = pygame.Surface(SCREEN.get_size(), pygame.SRCALPHA)
        pygame.draw.polygon(surf, LIGHTCOLOUR, points)
        x1, x2 = 200, 400
        if not x1 < x < x2:
            SCREEN.blit(surf, (0, 0))

while not TERMINATED:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            TERMINATED = True

    if not time.time() - LAST_TIME > DELAY:
        continue

    mouse_pos = pygame.mouse.get_pos()
    LAST_TIME = time.time()
    MOUSE_POS = mouse_pos
    LIGHTSOURCES[0] = MOUSE_POS

    SCREEN.fill((100, 100, 255))
    pygame.draw.rect(SCREEN, (0, 0, 0), RECT)
    pygame.draw.rect(SCREEN, (0, 0, 0), RECT2)
    draw_lighting()
    pygame.display.flip()

pygame.display.quit()
