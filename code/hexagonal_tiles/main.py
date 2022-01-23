# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 13:50:07 2022

@author: richa
"""
import random
from typing import List
from typing import Tuple

import pygame
from hexagon import HexagonTile

# pylint: disable=no-member


def create_hexagon(position, radius=50) -> HexagonTile:
    """Creates a hexagon tile at the specified position"""
    return HexagonTile(radius, position, colour=get_random_colour())


def get_random_colour(min_=150, max_=255) -> Tuple[int, ...]:
    """Returns a random RGB colour with each component between min_ and max_"""
    return tuple(random.choices(list(range(min_, max_)), k=3))


def init_hexagons(num_x=20, num_y=20) -> List[HexagonTile]:
    """Creates a hexaogonal tile map of size num_x * num_y"""
    # pylint: disable=invalid-name
    leftmost_hexagon = create_hexagon(position=(-30, -30))
    hexagons = [leftmost_hexagon]
    for x in range(num_x):
        if x:
            # alternate between bottom left and bottom right vertices of hexagon above
            index = 2 if x % 2 == 1 else 4
            position = leftmost_hexagon.vertices[index]
            leftmost_hexagon = create_hexagon(position)
            hexagons.append(leftmost_hexagon)

        # place hexagons to the left of leftmost hexagon, with equal y-values.
        hexagon = leftmost_hexagon
        for _ in range(num_y):
            x, y = hexagon.position  # type: ignore
            position = (x + hexagon.minimal_radius * 2, y)
            hexagon = create_hexagon(position)
            hexagons.append(hexagon)

    return hexagons


def render(screen, hexagons):
    """Renders hexagons on the screen"""
    screen.fill((0, 0, 0))
    for hexagon in hexagons:
        hexagon.render(screen)

    # draw borders around colliding hexagons and neighbours
    mouse_pos = pygame.mouse.get_pos()
    colliding_hexagons = [
        hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
    ]
    for hexagon in colliding_hexagons:
        for neighbour in hexagon.compute_neighbours(hexagons):
            neighbour.render_highlight(screen, border_colour=(100, 100, 100))
        hexagon.render_highlight(screen, border_colour=(0, 0, 0))
    pygame.display.flip()


def main():
    """Main function"""
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    hexagons = init_hexagons()
    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True

        for hexagon in hexagons:
            hexagon.update()

        render(screen, hexagons)
        clock.tick(50)
    pygame.display.quit()


if __name__ == "__main__":
    main()
