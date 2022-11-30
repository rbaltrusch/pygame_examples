# -*- coding: utf-8 -*-
"""Contains entity classes, such as Animal and Food"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from dataclasses import field
from functools import cached_property
from typing import Callable
from typing import DefaultDict
from typing import List
from typing import Optional
from typing import Tuple

import pygame
from src.coordinate import Coordinate
from src.search import SearchAlgorithm

# pylint: disable=c-extension-no-member


@dataclass
class FoodCloner:
    """Clones foods based on specified chance and dispersion parameters"""

    chance: float
    max_dispersion: float
    size_dispersion: float
    min_size: float
    max_size: float
    energy_dispersion: float
    max_length: int

    def clone(self, foods: List[Food], screen_size: Coordinate):
        """Adds clones of the specified foods to the foods list"""
        if not foods:
            return

        if len(foods) > self.max_length:
            return

        new_foods: List[Food] = []
        for food in foods:
            if self.chance <= random.random():
                continue

            new_position = Coordinate(
                self._compute_single_coordinate(screen_size.x, food.position.x),
                self._compute_single_coordinate(screen_size.y, food.position.y),
            )
            new_foods.append(self.create_new_food(food, new_position))
        foods.extend(new_foods)

    def _compute_single_coordinate(
        self, screen_dimension: float, food_coordinate: float
    ) -> float:
        half_dispersion = self.max_dispersion / 2
        max_ = screen_dimension - half_dispersion
        value = food_coordinate + self._get_random_dispersion_factor(
            self.max_dispersion
        )
        return min(max_, max(half_dispersion, value))

    def create_new_food(self, food: Food, position: Coordinate) -> Food:
        """Returns a new food at the specified position, based on the specified food"""
        size_factor = 1 + self._get_random_dispersion_factor(self.size_dispersion)
        energy_factor = 1 + self._get_random_dispersion_factor(self.energy_dispersion)
        return Food(
            size=max(self.min_size, min(self.max_size, size_factor * food.size)),
            energy=energy_factor * food.INITIAL_ENERGY,
            position=position,
            energy_decay=0.8 * energy_factor * food.energy_decay,
        )

    @staticmethod
    def _get_random_dispersion_factor(factor: float) -> float:
        return (random.random() - 0.5) * 2 * factor


@dataclass
class Food:  # pylint: disable=too-many-instance-attributes
    """Food entity class"""

    size: float
    energy: float
    energy_decay: float
    position: Coordinate
    _eaten: bool = field(init=False, default=False)

    base_food_colour: Tuple[int, int, int] = (255, 255, 255)
    food_quality_colour_factor: int = 20

    def __post_init__(self):
        self.INITIAL_ENERGY = self.energy  # pylint: disable=invalid-name

    def update(self):
        """Updates the food by decaying its energy"""
        self.energy -= max(0, self.energy_decay)

    def draw(self, screen: pygame.surface.Surface):
        """Draws the food on the screen"""
        pygame.draw.circle(screen, self.colour, tuple(self.position), self.size)

    def eat(self):
        """Sets the food status to eaten"""
        self._eaten = True

    @cached_property
    def colour(self) -> Tuple[int, int, int]:
        """Returns the current colour of the food (based on its quality and energy)"""
        r, g, b = self.base_food_colour  # pylint: disable=invalid-name
        offset = int(self.food_quality_colour_factor * self.energy)
        return (min(255, max(0, r - offset)), g, min(255, max(0, b - offset)))

    @property
    def dead(self) -> bool:
        """Returns True if the food is eaten or has no energy left in it, else False"""
        return self._eaten or self.energy <= 0


def move_towards(
    origin_position: Coordinate, destination_position: Coordinate, speed: float
):
    """Updates the specified origin_position by moving it towards the destination_position
    at the specified speed.
    """
    # pylint: disable=invalid-name
    x = destination_position.x - origin_position.x
    y = destination_position.y - origin_position.y
    distance = origin_position.compute_distance(destination_position)
    if not distance:
        return

    factor = min(speed / distance, 1)
    origin_position.x += x * factor
    origin_position.y += y * factor


@dataclass
class Animal:  # pylint: disable=too-many-instance-attributes
    """Animal entity class"""

    size: float
    speed: float
    food_size_factor: float
    position: Coordinate
    vision: int
    food_reach_distance: float
    energy_loss: float
    cloning_size: float
    search_algorithm: SearchAlgorithm
    random_position_generator: Callable[[], Coordinate]
    target_position: Optional[Coordinate] = field(init=False, default=None)
    base_animal_colour: Tuple[int, int, int] = (255, 100, 100)
    min_energy_loss = 0.1

    def update(
        self, foods: List[Food], foods_dict: DefaultDict[Coordinate, List[Food]]
    ):
        """Updates the animal by choosing a target, moving towards it, eating (if possible)
        and losing energy.
        """
        self.size -= max(
            self.min_energy_loss, self.energy_loss * self.speed * self.vision
        )
        target_positions = self._choose_target_position(foods)
        if target_positions is None:
            return

        self.target_position = target_positions[0]
        move_towards(self.position, self.target_position, self.speed)
        for target_position in target_positions:
            self._eat(foods_dict, target_position)

    def draw(self, screen: pygame.surface.Surface):
        """Draws the animal on the screen"""
        pygame.draw.circle(screen, self.colour, tuple(self.position), self.size)

    def _eat(
        self, foods: DefaultDict[Coordinate, List[Food]], target_position: Coordinate
    ):
        distance = self.position.compute_distance(target_position)  # type: ignore
        if distance > max(0, self.food_reach_distance):
            return

        foods_ = foods.get(target_position)  # type: ignore
        self.target_position = None
        if not foods_:
            return

        for food in foods_:
            if food.dead:
                continue
            # treating the entity as a square
            # each side grows by the square root of the total size increase
            self.size += math.sqrt(food.energy * self.food_size_factor)
            food.eat()

    def _choose_target_position(self, foods: List[Food]) -> List[Coordinate]:
        target_positions = self.search_algorithm.determine_target_position(
            self, foods, distance=self.vision
        )
        if target_positions is None:
            return [
                self.target_position
                if self.target_position is not None
                else self.random_position_generator()
            ]
        return target_positions

    @property
    def dead(self) -> bool:
        """Dead state of the animal, returns True if animal size is 0 or less"""
        return self.size <= 0

    @cached_property
    def colour(self) -> Tuple[int, int, int]:
        """Returns the colour of the animal"""
        return self.base_animal_colour
