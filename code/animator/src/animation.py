# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 18:03:43 2021

@author: richa
"""
import os

import pygame

EXTENSION = ".png"


class Animation:
    """Animation class. Animates images in a folder"""

    def __init__(
        self, folder="", position=(0, 0), alpha=(255, 255, 255), repeating=True
    ):
        self.images = []
        self.position = position
        self.repeating = repeating
        self.alpha = alpha
        self.active = True
        self.counter = 0
        self.set_folder(folder)

    def render(self, screen):
        """Renders the animation on the screen and updates the animation counter"""
        if not self.active:
            return

        if self.counter >= len(self.images) and self.repeating:
            self.counter = 0

        if self.counter < len(self.images):
            screen.blit(self.images[self.counter], self.position)
            self.counter += 1

    def set_folder(self, folder):
        """Sets the animation image folder"""
        if not os.path.isdir(folder):
            return

        self.folder = folder
        load = lambda path: pygame.image.load(path).convert_alpha()
        self.images = [
            load(os.path.join(folder, filename))
            for filename in os.listdir(folder)
            if filename.endswith(EXTENSION)
        ]
        for image in self.images:
            image.set_colorkey((self.alpha))

    def set_position(self, *position):
        """Sets the position of the animation"""
        self.position = position

    def set_repeating(self, repeating: str):
        """Sets the repeating attribute to True if repeating is 'on'"""
        self.repeating = repeating == "on"

    def set_alpha(self, *alpha):
        """Sets the passed colour as transparent for all images in the animation"""
        self.alpha = alpha
        self.set_folder(self.folder)
