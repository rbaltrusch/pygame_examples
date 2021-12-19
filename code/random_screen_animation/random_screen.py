# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 02:31:32 2020

Draws a random starry sky. Press ENTER to save the generated screen.

@author: Korean_Crimson
"""
import random

import pygame

# pylint: disable=no-member


def rand_screen(screen, colour):
    """Spawns a white 1x1 rect at a random screen location"""
    # pylint: disable=invalid-name
    x = random.randint(0, screen.get_width())
    y = random.randint(0, screen.get_height())
    rect = pygame.Rect(x, y, 1, 1)
    pygame.draw.rect(screen, colour, rect, width=0)


def main():
    """Main function"""
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))
    screen.fill((0, 0, 55))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RETURN]:
            pygame.image.save(screen, "animation/generated_screen.png")
            print("saved to disk")

        rand_screen(screen, colour=(255, 255, 255))
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
