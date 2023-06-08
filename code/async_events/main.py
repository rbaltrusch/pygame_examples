# -*- coding: utf-8 -*-
"""Asynchronous event handling using generators"""

# pylint: disable=no-member
# pylint: disable=invalid-name
# pylint: disable=c-extension-no-member

import time
from typing import Any, Generator, List, Optional, Callable, Tuple
from dataclasses import dataclass

import pygame

Event = Generator[None, None, None]
Callback = Callable[[], Any]
Colour = Tuple[int, int, int]


class Delay:
    """
    Iterable delay class that can be used in an asynchronous event to delay for an amount of time.
    Can be used like this to asynchronously delay by 1 second: yield from Delay(1)
        Note: this is equivalent to the following: for _ in Delay(1): yield
    An optional wait_callback can be specified, which will be called each tick while delaying.
    """

    def __init__(self, duration: float, wait_callback: Optional[Callback] = None):
        self.duration = duration
        self.wait_callback = wait_callback
        self.start_time = time.time()

    def __iter__(self):
        while time.time() - self.start_time < self.duration:
            if self.wait_callback:
                self.wait_callback()
            yield


class EventQueue:
    """
    Encapsulates the asynchronous event handling by handling a single generated
    result per event per tick.
    """

    def __init__(self):
        self._events: List[Event] = []

    def update(self) -> None:
        """Updates the event queue"""
        expired_events: List[Event] = []
        for event in self._events:
            try:
                next(event)
            except StopIteration:
                expired_events.append(event)
        self._events = [x for x in self._events if x not in expired_events]

    def append(self, event: Event) -> None:
        """Appends the specified event to the event queue"""
        self._events.append(event)


@dataclass
class Player:
    """Example player class (unrelated to asynchronous events)"""

    x: int
    y: int
    colour: Colour
    visible: bool = True

    def render(self, screen: pygame.surface.Surface) -> None:
        """Renders the player on the screen"""
        if not self.visible:
            return
        pygame.draw.rect(screen, self.colour, (self.x, self.y, 25, 25))  # type: ignore


def change_background_colour(screen: pygame.surface.Surface) -> Event:
    """Async event changing the background colour first to red, then to white"""
    yield from Delay(0.5, wait_callback=lambda: screen.fill((255, 0, 0)))
    yield from Delay(0.5, wait_callback=lambda: screen.fill((255, 255, 255)))


def move_player(player: Player) -> Event:
    """Async event to move the player by several steps in the x direction"""
    player.x += 5
    yield from Delay(0.3)
    player.x += 10
    yield from Delay(0.3)
    player.x += 15


def hurt_player(player: Player) -> Event:
    """Async event to toggle player visibility a few times"""
    visible_values = [False, True] * 3
    for visible in visible_values:
        player.visible = visible
        yield from Delay(0.3)


def wobble_player(player: Player) -> Event:
    """Async event to animate player gently shifting up and down"""
    offsets = [0, 2, 2, 1, 0, -1, -2, -2, -2, -2, -1, 0, 1, 2, 2] * 3
    for offset in offsets:
        player.y += offset
        yield from Delay(0.05)


def main():
    """Main function"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    event_queue = EventQueue()
    player = Player(x=0, y=150, colour=(200, 200, 200))
    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    event_queue.append(change_background_colour(screen))
                if event.key == pygame.K_h:
                    event_queue.append(hurt_player(player))
                if event.key == pygame.K_m:
                    event_queue.append(move_player(player))
                if event.key == pygame.K_w:
                    event_queue.append(wobble_player(player))
        screen.fill((0, 0, 0))
        event_queue.update()
        player.render(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
