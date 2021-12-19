# -*- coding: utf-8 -*-
"""
Created on Tue May 11 17:52:41 2021

A squish and stretch test, which loads a large image, then scales its size
depending on the current mouse position.

@author: Korean_Crimson
"""
# pylint: disable=no-member
import pygame


def main():
    """Main function"""
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    surface = pygame.image.load("image.png")

    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True

        screen.fill((100, 100, 255))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        size = (600 - mouse_x, 400 - mouse_y)
        rect = pygame.Rect(mouse_x, mouse_y, *size)
        scaled_surface = pygame.transform.scale(surface, size)
        screen.blit(scaled_surface, rect)
        pygame.display.flip()
        clock.tick(50)

    pygame.display.quit()


if __name__ == "__main__":
    main()
