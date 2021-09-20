# -*- coding: utf-8 -*-
"""
Created on Sun May 16 18:46:57 2021

@author: Korean_Crimson
"""

import os
import pygame
from client import Network

pygame.init() #pylint: disable=no-member
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
surf = pygame.image.load(os.path.join("media", "image.png"))
rect = surf.get_rect()
network = Network()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        pass
    data = network.send('get')
    if data:
        speed = [int(x) for x in data.split(',')]
        print(speed)
        rect = rect.move(speed)
    print(data)
    screen.fill((0, 0, 0))
    screen.blit(surf, rect)
    pygame.display.flip()
