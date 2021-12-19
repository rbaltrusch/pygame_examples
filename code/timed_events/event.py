# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 15:35:16 2020

This example showcases how one might code an event handling system in python,
which could be used in a game written with pygame.

The event is a function with an arbitrary amount of passed arguments, being
executed after a specified time delay. This event-based approach significantly
reduces coupling in game code.

@author: Korean_Crimson
"""
from __future__ import annotations

import functools
import time
from dataclasses import dataclass
from typing import Callable

import pygame

SCREEN_HEIGHT = (800, 600)

# pylint: disable=no-member


@dataclass
class Event:
    """Event class. When the specified delay elapsed, the specified
    function will get executed when the event is handled."""

    function: Callable
    timer: Timer

    def __post_init__(self):
        self.timer.start()


class Timer:
    """A timer class, which gets started at a time and counts until a specified delay has passed"""

    def __init__(self, delay):
        self.time = 0
        self.delay = delay

    def start(self):
        """Starts the timer"""
        self.time = time.time()

    def get_timer(self):
        """Returns True if time since start time is over the delay, else False"""
        return time.time() - self.time > self.delay


class Entity:
    """Simplistic entity class. For this example only has an event_queue attribute"""

    def __init__(self):
        self.event_queue = []

    def add_event(self, function, delay):
        """Adds an event with the specified function and delay to the event queue"""
        self.event_queue.append(Event(function, delay))

    def handle_events(self):
        """Handles all events in the event queue. Removes handled events from the event queue"""
        for event in self.event_queue:
            if event.timer.get_timer():
                event.func()
                self.event_queue.remove(event)


def event_function(entity):
    """Example function linked to the event"""
    print(time.time())
    func = functools.partial(event_function, entity)
    entity.add_event(func, 1)


def main():
    """Main function, initiates an entity with a 1 second cyclic event function"""
    pygame.init()
    pygame.display.set_mode(SCREEN_HEIGHT)

    entity = Entity()
    func = functools.partial(event_function, entity)
    entity.add_event(func, 1)

    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
        entity.handle_events()
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
