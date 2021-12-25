# -*- coding: utf-8 -*-
"""
Created on Tue May 11 17:52:41 2021

A game loop with a simple in-game console (press-ENTER).

The console here currently supports one command, which sets the background colour
to the provided r g b values (int):
    /bg r g b

@author: Korean_Crimson
"""
# pylint: disable=no-member
import argparse
import os

import pygame

BACKGROUND_COLOUR = (0, 0, 0)

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
class Text:
    """Text class"""

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
        """Renders the text"""
        rect = pygame.Rect(*self.position, *self.size)
        pygame.draw.rect(screen, self.background_colour, rect)

        lines = self.text.split("\n")
        x, y = self.position  # pylint: disable=invalid-name
        for i, line in enumerate(lines):
            rendered_text = self.font.render(line, True, self.text_colour)
            screen.blit(rendered_text, (x, y + i * self.line_height))


class Console:
    """Game console"""

    def __init__(self, parser, text: Text):
        self.parser = parser
        self.text = text
        self.active = False
        self.text_buffer = []

    def toggle_activate(self):
        """Toggles the active state of the console"""
        self.active = not self.active

    def execute(self):
        """Parses the arguments in the console text buffer"""
        text = "".join(self.text_buffer)
        self.parser.parse_args(text.split())
        self.flush()

    def render(self, screen):
        """Renders the console"""
        if not self.active:
            return
        self.text.text = "".join(self.text_buffer)
        self.text.render(screen)

    def add_text(self, text: str):
        """Adds a character ot the text buffer"""
        self.text_buffer.append(text)

    def flush(self):
        """Empties the text buffer"""
        self.text_buffer = []

    def remove_last_char(self):
        """Removes the last character from the text buffer"""
        if self.text_buffer:
            self.text_buffer.pop(-1)


class BgAction(argparse.Action):
    """Background action, sets the background colour to the specified value when
    /bg arg is specified.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        global BACKGROUND_COLOUR  # pylint: disable=global-statement
        BACKGROUND_COLOUR = values


def get_parser_help_message(parser):
    """Returns the help string from the parser"""
    with open("temp.txt", "w+") as file:
        parser.print_help(file)
    with open("temp.txt", "r") as file:
        contents = file.read()
    os.remove("temp.txt")
    return contents


def init_console():
    """Initialises the game console"""
    font = pygame.font.SysFont("Courier", 12)
    text = Text(font, size=(200, 40), position=(0, 0))
    return Console(init_parser(), text)


def init_parser():
    """Initialises the argument parser"""
    parser = argparse.ArgumentParser(description="Game console", prefix_chars="/")
    parser.add_argument("/bg", nargs=3, type=int, action=BgAction)
    return parser


def init_error_message(console):
    """Initialises the error message"""
    font = pygame.font.SysFont("Courier", 12)
    contents = get_parser_help_message(console.parser)
    return Text(
        font,
        size=(400, 200),
        text=contents,
        position=(100, 100),
        background_colour=(207, 102, 121),
    )


def update_console(console):
    """Updates the game console"""
    console.toggle_activate()
    error_message = None
    if not console.active:
        try:
            console.execute()
        except SystemExit:
            error_message = init_error_message(console)
            console.flush()
    return error_message


def main():
    """Main function"""
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    console = init_console()
    error_message = None
    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                error_message = update_console(console)
            elif event.type == pygame.TEXTINPUT and console.active:
                console.add_text(event.text)
            elif (
                event.type == pygame.KEYUP
                and event.key == pygame.K_BACKSPACE
                and console.active
            ):
                console.remove_last_char()
            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                error_message = None

        screen.fill(BACKGROUND_COLOUR)
        console.render(screen)
        if error_message is not None:
            error_message.render(screen)
        pygame.display.flip()
        clock.tick(50)

    pygame.display.quit()


if __name__ == "__main__":
    main()
