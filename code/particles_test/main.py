# -*- coding: utf-8 -*-
"""
Created on Sun May  2 20:52:31 2021

Showcases three different particle effects. Jump from one to the next by pressing
the close window button.

@author: Korean_Crimson
"""

import random
import time
import pygame

PARTICLES = [] #contains all particles
STARTSIZE = 25 #start size of the particle
DELAY = 0.02 #fixes framerate to 50 fps
WIDTH = 0 #0 for a fully-coloured particle, or a positive int for a bordered particle

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
        """Play around with the update function to get various particle effects"""
        if self.size > 0:
            self.size -= 1
        else:
            self.expired = True
        self._update_colour()
        self.x += 2
        self.y += 2

    def draw(self):
        if not self.expired:
            rect = pygame.Rect(self.x, self.y, self.size, self.size)
            pygame.draw.rect(SCREEN, self.colour, rect, self.width)

    def _update_colour(self):
        r,g,b = self.colour
        blue = b - 2 if b >= 2 else 0
        self.colour = [r, g, blue]

class FadingRectParticle(RectParticle):
    def _update_colour(self):
        """Overrides RectParticle._update_colour"""
        self.colour = [c - 5 if c >= 5 else 0 for c in self.colour]
        
class CircleParticle(RectParticle):
    def draw(self):
        if not self.expired:
            pygame.draw.circle(SCREEN, self.colour, (self.x, self.y), self.size)

def draw_particles(mouse_pos, particle_type, colour):
    """Appends a new particle at the mouse_position, of the specified type and colour"""
    PARTICLES.append(particle_type(*mouse_pos, STARTSIZE, colour, WIDTH))

def init():
    """Initialises the pygame display"""
    global SCREEN
    pygame.init()
    SCREEN = pygame.display.set_mode((600, 400))

def main(particle_type, colour):
    """Runs the particle effect, accepts a particle_type (class object) and a colour (rgb tuple)"""
    previous_mouse_pos = pygame.mouse.get_pos()
    previous_time = time.time()

    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
    
        if not time.time() - previous_time > DELAY:
            continue
    
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos != previous_mouse_pos:
            draw_particles(mouse_pos, particle_type, colour)
        previous_time = time.time()
        previous_mouse_pos = mouse_pos
    
        SCREEN.fill((0, 0, 0))
        for particle in PARTICLES:
            particle.update()
            particle.draw()
        pygame.display.flip()


if __name__ == '__main__':
    init()

    #blue rectangular particle effect
    main(particle_type=RectParticle, colour=(100, 100, 255))

    #red circular particle effect
    main(particle_type=CircleParticle, colour=(255, 100, 100))

    #fading white rectangular particle effect
    main(particle_type=FadingRectParticle, colour=(255, 255, 255))

    pygame.display.quit()
