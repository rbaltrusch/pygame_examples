# -*- coding: utf-8 -*-
"""
Created on Fri May  7 21:43:50 2021

Short draft of how a lighting system could be implemented in pygame.
Currently only supports light incident on a surface without shadows.

@author: Korean_Crimson
"""

import math
import pygame

#pylint: disable=no-member
#pylint: disable=invalid-name

DELAY = 0.02
LIGHTINTENSITY = 0
LIGHTCOLOUR = (255, 255, 153, 100)

def distance(point1, point2):
    """Returns the distance (int) between two (x, y) tuples"""
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def draw_x_side_lighting(light_source, midpoints_x, vertices):
    """Draws light from source to vertical sides of the rect"""
    _, y = light_source
    _, min_x = min([(distance(light_source, point), point) for point in midpoints_x])
    xdistances = [distance(min_x, v) for v in vertices]
    xpoints, _ = zip(*sorted(zip(vertices, xdistances), key=lambda x: x[1]))
    points = [light_source, *xpoints[:2]]

    surf = pygame.Surface(SCREEN.get_size(), pygame.SRCALPHA)
    pygame.draw.polygon(surf, LIGHTCOLOUR, points)
    y1, y2 = 200, 400 #HACK
    if not y1 < y < y2:
        SCREEN.blit(surf, (0, 0))

def draw_y_slide_lighting(light_source, midpoints_y, vertices):
    """Draws light from source to horizontal sides of the rect"""
    x, _ = light_source
    _, min_y = min([(distance(light_source, point), point) for point in midpoints_y])
    ydistances = [distance(min_y, v) for v in vertices]
    ypoints, _ = zip(*sorted(zip(vertices, ydistances), key=lambda x: x[1]))
    points = [light_source, *ypoints[:2]]

    surf = pygame.Surface(SCREEN.get_size(), pygame.SRCALPHA)
    pygame.draw.polygon(surf, LIGHTCOLOUR, points)
    x1, x2 = 200, 400 #HACK
    if not x1 < x < x2:
        SCREEN.blit(surf, (0, 0))

def draw_lighting(light_sources):
    """Draws lighting for each light source"""
    #HACK: sides of the black square. Implement function that determines the midpoints and vertices!
    midpoints_x = [(300, 200), (300, 400)]
    midpoints_y = [(200, 300), (400, 300)]
    vertices = [(200, 200), (200, 400), (400, 200), (400, 400)]
    for light_source in light_sources:
        draw_x_side_lighting(light_source, midpoints_x, vertices)
        draw_y_slide_lighting(light_source, midpoints_y, vertices)

def init():
    """Initialises the pygame display and clock"""
    #pylint: disable=global-variable-undefined
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((600, 400))
    CLOCK = pygame.time.Clock()

def update_screen(objects, light_sources):
    """Updates a number of objects and light sources on the screen"""
    SCREEN.fill((100, 100, 255))
    for object_ in objects:
        pygame.draw.rect(SCREEN, (0, 0, 0), object_)
    draw_lighting(light_sources)
    pygame.display.flip()

def main():
    """Main function, draws a number of objects and light sources on the screen"""
    objects = [pygame.Rect(200, 200, 200, 200), pygame.Rect(100, 0, 50, 400)]
    light_sources = [(300, 300), (0, 0)] #points from where light comes in the scene

    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
        light_sources[0] = pygame.mouse.get_pos()
        update_screen(objects, light_sources)
        CLOCK.tick(50)

    pygame.display.quit()

if __name__ == '__main__':
    init()
    main()
