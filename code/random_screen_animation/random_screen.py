# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 02:31:32 2020

Draws a random starry sky. Press ENTER to save the generated screen.

@author: Korean_Crimson
"""

import random
import pygame

def rand_screen(screen, colour):
    """Spawns a white 1x1 rect at a random screen location"""
    x = random.randint(0, screen.get_width())
    y = random.randint(0, screen.get_height())
    rect = pygame.Rect(x, y, 1, 1)
    pygame.draw.rect(screen, colour, rect, width=0)

def main():
    """Main function"""
    CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((800, 600))
    SCREEN.fill((0,0,55))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RETURN]:
            pygame.image.save(SCREEN, "animation/generated_screen.png")
            print("saved to disk")

        rand_screen(SCREEN, colour=(255, 255, 255))
        pygame.display.flip()
        CLOCK.tick(10)

    pygame.quit()

if __name__ == '__main__':
    main()
