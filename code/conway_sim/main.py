"""An implementation of Conway's game of life."""

from __future__ import annotations

from dataclasses import dataclass
import itertools
import random
from typing import Dict, List, Optional, Tuple

import pygame

# pylint: disable=no-member

Position = Tuple[int, int]
Colour = Tuple[int, int, int]

NEIGHBOUR_OFFSETS = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
)
# B3/S23, B6/S16, B36/S23
BIRTH_NEIGHBOUR_AMOUNTS = (3,)
SURVIVAL_NEIGHBOUR_AMOUNTS = (2, 3)


@dataclass
class Cell:
    """A Conway cell."""

    position: Position
    colour: Colour

    def __post_init__(self):
        self.alive: bool = True

    SIZE = 20

    def update(self, cells: Dict[Position, Cell]) -> None:
        """Updates the cell using the rules of Conway's game of life."""
        neighbours = determine_neighbours(cells, self.position)
        amount_of_neighbours = len(neighbours)
        if not amount_of_neighbours in SURVIVAL_NEIGHBOUR_AMOUNTS:
            self.alive = False

    def at(self, x: int, y: int) -> Cell:
        """Creates a new identical cell at the specified position"""
        return Cell(position=(x, y), colour=self.colour)

    def render(self, surface: pygame.surface.Surface) -> None:
        """Renders the cell."""
        x, y = self.position
        rect = pygame.Rect(x * self.SIZE, y * self.SIZE, self.SIZE, self.SIZE)
        pygame.draw.rect(surface, self.colour, rect)
        # pygame.draw.circle(surface, self.colour, (x * self.SIZE, y * self.SIZE), self.SIZE, width=1)


class Board:
    """Used to render a grid with some cells on it."""

    def __init__(self, width: int, height: int, empty_cell: Cell):
        self.width = width
        self.height = height
        self.empty_cell = empty_cell

    def render(
        self, cells: Dict[Position, Cell], surface: pygame.surface.Surface
    ) -> None:
        """Renders the cells on the board."""
        for x, y in itertools.product(range(self.width), range(self.height)):
            #cell = cells.get((x, y)) or self.empty_cell.at(x, y)
            cell = cells.get((x, y))
            if cell:
                cell.render(surface)


def determine_neighbours(cells: Dict[Position, Cell], position: Position) -> List[Cell]:
    """Returns the neighbours of the cell at the specified position."""
    x, y = position
    positions = ((x + x2, y + y2) for x2, y2 in NEIGHBOUR_OFFSETS)
    optional_cells = (cells.get(pos) for pos in positions)
    return list(filter(None, optional_cells))


def average_colour(colours: List[Optional[Colour]]) -> Colour:
    """
    Returns the average colour of all specified colours passed,
    or a random new colour if none were passed.
    """
    actual_colours = [x for x in colours if x is not None]
    if not actual_colours:
        return _get_random_colour()
    # return random.choice(actual_colours)
    # limit to 2 to avoid colour over time averaging to a grey goo
    return tuple(int(sum(x) / len(x)) for x in zip(*actual_colours[:2]))  # type: ignore


def create_new_cells(cells: Dict[Position, Cell], width: int, height: int) -> None:
    """
    Creates new cells based on existing cells for Conway rule #4:
    dead cells with exactly 3 neighbours come alive.
    """
    for position in itertools.product(range(width), range(height)):
        neighbours = determine_neighbours(cells, position)
        if len(neighbours) not in BIRTH_NEIGHBOUR_AMOUNTS:
            continue
        cells[position] = Cell(
            position, colour=average_colour([x.colour for x in neighbours])
        )


def _get_random_colour() -> Colour:
    return tuple(random.randint(0, 255) for _ in range(3))  # type: ignore


def spawn_cells(amount: int, width: int, height: int) -> Dict[Position, Cell]:
    """
    Spawns a specified amount of cells, with randomly spread out
    positions of the specified width and height.
    """
    positions = [
        (random.randint(0, width), random.randint(0, height)) for _ in range(amount)
    ]
    return {
        position: Cell(position, colour=_get_random_colour()) for position in positions
    }


def update_cells(
    cells: Dict[Position, Cell], width: int, height: int
) -> Dict[Position, Cell]:
    """Updates the cells according to Conway's rules and returns a set of updated cells."""
    for cell in cells.values():
        cell.update(cells)

    create_new_cells(cells, width=width, height=height)
    _cells = [(pos, cell) for pos, cell in cells.items() if cell.alive]
    random.shuffle(_cells)
    cells = {pos: cell for pos, cell in _cells}
    return cells


def main():
    """Main function"""
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    Cell.SIZE = 6  # type: ignore
    clock = pygame.time.Clock()
    board = Board(
        width=100, height=100, empty_cell=Cell(position=(0, 0), colour=(0, 0, 0))
    )
    cells = spawn_cells(amount=250, width=board.width, height=board.height)
    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminated = True
                elif event.key == pygame.K_r:
                    cells = spawn_cells(amount=250, width=board.width, height=board.height)

        cells = update_cells(cells, board.width, board.height)

        # changing some colours for colour variety
        for i, cell in enumerate(cells.values()):
            if i > 10:
                break
            cell.colour = _get_random_colour()

        screen.fill((0, 0, 0))
        # screen.fill((50, 50, 50), special_flags=pygame.BLEND_RGBA_SUB)
        board.render(cells, screen)
        pygame.display.flip()
        clock.tick(30)
    pygame.display.quit()


if __name__ == "__main__":
    main()
