# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 18:24:52 2021

@author: richa
"""
import argparse
import os

import pygame
from src.animation import Animation
from src.console import Console
from src.event_queue import EventQueue
from src.event_queue import get_action
from src.text import Text


def init():
    """Initialises the event queue, the console and the animation"""
    event_queue = EventQueue()
    parser = init_parser(event_queue)
    console = init_console(parser)
    animation = init_animation(event_queue)
    return animation, event_queue, console


def init_parser(event_queue):
    """Initialises the parser"""
    parser = argparse.ArgumentParser(
        description="Game console interface", prefix_chars="/"
    )
    parser.add_argument(
        "/folder",
        "/f",
        type=str,
        action=get_action(event_queue, "SET_FOLDER"),
        help="set folder containing animation images",
    )
    parser.add_argument(
        "/alpha",
        "/a",
        nargs=3,
        type=int,
        action=get_action(event_queue, "SET_ALPHA"),
        help="set colour to be made transparent",
    )
    parser.add_argument(
        "/fps",
        type=int,
        action=get_action(event_queue, "SET_FPS"),
        help="sets animation fps",
    )
    parser.add_argument(
        "/repeat",
        nargs="?",
        choices=["on", "off"],
        default="on",
        action=get_action(event_queue, "SET_REPEAT"),
        help="sets repeating animation on or off",
    )
    parser.add_argument(
        "/position",
        "/pos",
        nargs=2,
        type=int,
        action=get_action(event_queue, "SET_POSITION"),
        help="sets the position of the animation",
    )
    return parser


def init_console(parser):
    """Initialises the console"""
    font = pygame.font.SysFont("Courier", 12)
    text = Text(font, size=(200, 40), position=(0, 0))
    error_text = init_error_message(parser)
    return Console(parser, text, error_text)


def init_error_message(parser):
    """Initialises the error message"""
    font = pygame.font.SysFont("Courier", 12)
    contents = get_parser_help_message(parser)
    return Text(
        font,
        size=(400, 200),
        text=contents,
        position=(100, 100),
        background_colour=(207, 102, 121),
    )


def get_parser_help_message(parser):
    """Returns the help message from the parser"""
    with open("temp.txt", "w+") as file:
        parser.print_help(file)
    with open("temp.txt", "r") as file:
        contents = file.read()
    os.remove("temp.txt")
    return contents


def init_animation(event_queue):
    """Initialises the animation"""
    path = os.path.dirname(__file__)
    directories = [
        os.path.join(path, p)
        for p in os.listdir(path)
        if os.path.isdir(os.path.join(path, p))
    ]
    folder = directories[0] if directories else ""
    animation = Animation(folder)

    event_queue.subscribe("SET_FOLDER", animation.set_folder)
    event_queue.subscribe("SET_ALPHA", animation.set_alpha)
    event_queue.subscribe("SET_REPEAT", animation.set_repeating)
    event_queue.subscribe("SET_POSITION", animation.set_position)
    return animation
