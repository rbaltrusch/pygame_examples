# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 18:03:13 2021

@author: richa
"""
import pygame


class Text:
    def __init__(
        self,
        font,
        size,
        position,
        line_height=20,
        text="",
        text_colour=(255, 255, 255),
        background_colour=(50, 50, 50),
    ):
        self.text = text
        self.font = font
        self.size = size
        self.position = position
        self.text_colour = text_colour
        self.background_colour = background_colour
        self.line_height = line_height

    def render(self, screen):
        rect = pygame.Rect(*self.position, *self.size)
        pygame.draw.rect(screen, self.background_colour, rect)

        lines = self.text.split("\n")
        x, y = self.position
        for i, line in enumerate(lines):
            rendered_text = self.font.render(line, True, self.text_colour)
            screen.blit(rendered_text, (x, y + i * self.line_height))
