# -*- coding: utf-8 -*-
"""
Created on Sun May 16 18:46:57 2021

@author: Korean_Crimson
"""
import pygame
from client import Network

# pylint: disable=no-member

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((100, 100))
network = Network()


def get_speed(keys):
    """Returns the speed as a string depending on the key state. This can be
    sent directly to the server to communicate this speed to another machine.
    """
    if keys[pygame.K_LEFT]:
        speed = "-1,0"
    elif keys[pygame.K_RIGHT]:
        speed = "1,0"
    elif keys[pygame.K_DOWN]:
        speed = "0,1"
    elif keys[pygame.K_UP]:
        speed = "0,-1"
    else:
        speed = "0,0"
    return speed


def main():
    """Main function"""
    while True:
        pygame.event.get()
        keys = pygame.key.get_pressed()
        speed = get_speed(keys)
        network.send(f"set:{speed}")
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
