# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 18:20:59 2021

@author: richa
"""
from src.text import Text


class Console:
    """Console class"""

    def __init__(self, parser, text: Text, error_text: Text):
        self.parser = parser
        self.text = text
        self.error_text = error_text
        self.errored = False
        self.active = False
        self.text_buffer = []

    def toggle_activate(self):
        """Toggles the active state of the console"""
        self.active = not self.active

    def execute(self):
        """Executes the entered commands using the parser. Displays the error
        message if the entered commands cannot be parsed.
        """
        try:
            text = "".join(self.text_buffer)
            self.flush()
            self.parser.parse_args(text.split())
            self.errored = False
        except SystemExit:
            self.error_out()

    def error_out(self):
        """Sets errored to True and flushes the text buffer"""
        self.errored = True
        self.flush()

    def render(self, screen):
        """Renders the console on the screen"""
        if self.errored:
            self.error_text.render(screen)

        if not self.active:
            return

        self.text.text = "".join(self.text_buffer)
        self.text.render(screen)

    def add_text(self, text: str):
        """Adds a character to the end of the text buffer"""
        self.text_buffer.append(text)

    def flush(self):
        """Removes all characters from the text buffer"""
        self.text_buffer = []

    def remove_last_char(self):
        """Removes the last character in the text buffer"""
        if self.text_buffer:
            self.text_buffer.pop(-1)
