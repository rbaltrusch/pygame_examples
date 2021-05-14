# -*- coding: utf-8 -*-
"""
Created on Sun May  2 20:52:31 2021

@author: Korean_Crimson
"""

import random
import time
import pygame

TERMINATED = False

pygame.init()
SCREEN = pygame.display.set_mode((600, 400))
MOUSE_POS = pygame.mouse.get_pos()
PARTICLES = []
STARTSIZE = 25
DELAY = 0.02
LAST_TIME = time.time()
COLOUR = (100, 100, 255)
WIDTH = 0

class RectParticle:
    def __init__(self, x, y, size, colour, width):
        self.x = x + random.randint(-20, 20)
        self.y = y + random.randint(-20, 20)
        self.size = size
        self.colour = [rgb - random.randint(0, 35) for rgb in colour]
        self.colour = colour
        self.width = width
        self.expired = False

    def update(self):
        if self.size > 0:
            self.size -= 1
        else:
            self.expired = True
        # self.colour = [c - 5 for c in self.colour]
        r,g,b = self.colour
        self.colour = [r, g, b - 2]
        self.x += 2
        self.y += 2

    def draw(self):
        if not self.expired:
            rect = pygame.Rect(self.x, self.y, self.size, self.size)
            pygame.draw.rect(SCREEN, self.colour, rect, self.width)

class CircleParticle(RectParticle):
    def draw(self):
        if not self.expired:
            pygame.draw.circle(SCREEN, self.colour, (self.x, self.y), self.size)

def draw_particles():
    PARTICLES.append(RectParticle(*MOUSE_POS, STARTSIZE, COLOUR, WIDTH))

while not TERMINATED:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            TERMINATED = True

    if not time.time() - LAST_TIME > DELAY:
        continue

    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos != MOUSE_POS:
        draw_particles()
    LAST_TIME = time.time()
    MOUSE_POS = mouse_pos

    SCREEN.fill((0, 0, 0))
    for particle in PARTICLES:
        particle.update()
        particle.draw()
    pygame.display.flip()

pygame.display.quit()
