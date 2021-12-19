# -*- coding: utf-8 -*-
"""
Created on Sun May 16 18:46:57 2021

@author: Korean_Crimson
"""
import pygame
from client import Network

# pylint: disable=no-member
def main():
    """Main function"""
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    rect = pygame.Rect(0, 0, 50, 50)
    network = Network()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        data = network.send("get")
        print(data)
        if data and "," in data:
            speed = [int(x) for x in data.split(",")]
            rect = rect.move(speed)

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), rect)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
