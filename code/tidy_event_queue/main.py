# -*- coding: utf-8 -*-
"""
Created on Tue May 11 17:52:41 2021

A squish and stretch test, which loads a large image, then scales its size
depending on the current mouse position.

@author: Korean_Crimson
"""
# pylint: disable=no-member
import math
from collections import defaultdict
from dataclasses import dataclass
from functools import partial
from typing import Callable
from typing import Tuple

import pygame

COLOUR = (0, 0, 0)


class EventQueue:
    """Event queue class that contains events. Events can be subscribed to call a callback"""

    def __init__(self):
        self.events = []
        self.subscribers = defaultdict(list)

    def subscribe(self, event_id: int, function: Callable):
        """Subscribes the passed function to the event. Whenever the named event
        occurs, the passed function will be executed.
        """
        self.subscribers[event_id].append(function)

    def pump(self, event: pygame.event.Event):
        """Adds an event to the end of the events list"""
        self.events.append((event))

    def update(self):
        """Calls all subscriber functions for all pumped events, then removes all pumped events."""
        for event in self.events:
            for function in self.subscribers[event.type]:
                # pass the pygame event to the callback functions attached to this event_id
                function(event)
        self.events = []


@dataclass
class State:
    """Class keeping some state to be passed to callbacks.
    Could also use globals or split this up into multiple classes if required.
    """

    screen: pygame.Surface
    previous_screen: pygame.Surface = None
    draw: bool = False
    radius: float = 1.0
    center: Tuple[int, int] = (0, 0)
    terminated: bool = False


def draw(state: State, event):
    """Callback for pygame.MOUSEBUTTONDOWN event"""
    state.draw = True
    state.previous_screen = state.screen.copy()
    state.center = event.pos
    pygame.draw.circle(state.screen, COLOUR, state.center, state.radius, width=1)


def no_draw(state: State, _):
    """Callback for pygame.MOUSEBUTTONUP event"""
    state.draw = False
    state.radius = 1


def extend(state: State, event):
    """Callback for pygame.MOUSEMOTION event"""
    # pylint: disable=invalid-name
    if not state.draw:
        return

    if state.previous_screen is not None:
        state.screen.blit(state.previous_screen, (0, 0))
        pygame.display.flip()

    x1, y1 = state.center
    x2, y2 = event.pos
    state.radius = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)  # pythagoras
    print(state.radius)
    pygame.draw.circle(state.screen, COLOUR, state.center, state.radius, width=1)


def quit_(state: State, _):
    """Callback for pygame.QUIT event"""
    state.terminated = True


def main():
    """Main function"""
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    screen.fill((255, 255, 255))
    clock = pygame.time.Clock()
    state = State(screen)

    # sets up the event queue with the various pygame events to be tracked
    event_queue = EventQueue()
    event_queue.subscribe(pygame.MOUSEBUTTONDOWN, function=partial(draw, state))
    event_queue.subscribe(pygame.MOUSEBUTTONUP, function=partial(no_draw, state))
    event_queue.subscribe(pygame.MOUSEMOTION, function=partial(extend, state))
    event_queue.subscribe(pygame.QUIT, function=partial(quit_, state))

    while not state.terminated:
        for event in pygame.event.get():
            event_queue.pump(event)
        event_queue.update()
        pygame.display.flip()
        clock.tick(50)

    pygame.display.quit()


if __name__ == "__main__":
    main()
