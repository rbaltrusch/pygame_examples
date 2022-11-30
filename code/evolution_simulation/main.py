# -*- coding: utf-8 -*-
"""Evolution simulation of animals hunting for food.
Press Escape to exit, ENTER to init new simulation.
"""
from __future__ import annotations

import copy
import random
import statistics
from collections import defaultdict
from typing import DefaultDict
from typing import List

import pygame
from src.coordinate import Coordinate
from src.entity import Animal
from src.entity import Food
from src.entity import FoodCloner
from src.params import AnimalParams
from src.params import FoodParams
from src.params import RunnerParams
from src.params import Stat
from src.plotting import plot_data
from src.plotting import PlotData
from src.search import PositionBinner
from src.search import PositionClusterer
from src.search import SearchAlgorithm
from src.search import SimplePositionClusterer
from src.search import SimplePositionLerper

SEED = random.randint(0, 10000)
FRAMERATE = 60
SCREEN_SIZE = Coordinate(800, 600)
ANIMAL_CLONE_DISPERSION = 50
ANIMAL_VISION_DISPERSION = 20
ANIMAL_COLOUR_DISPERSION = 20
ANIMAL_CLONING_SIZE_FACTOR = 0.7
RANDOM_NEW_ANIMAL_CHANCE = 0.3


def generate_random_position(screen_offset: int = 0) -> Coordinate:
    """Generates a random position on the screen. The minimum distance to the screen borders
    can be specified using the optional screen_offset parameter.
    """
    return Coordinate(
        random.randint(screen_offset, int(SCREEN_SIZE.x) - screen_offset),
        random.randint(screen_offset, int(SCREEN_SIZE.y) - screen_offset),
    )


def init_foods(params: FoodParams, clusterer: PositionClusterer) -> List[Food]:
    """Initialises a list of foods in random clustered positions using the specified parameters"""
    positions = [
        generate_random_position(params.screen_offset)
        for _ in range(params.initial_amount)
    ]
    clustered_positions = clusterer.cluster_positions(positions)

    return [
        Food(
            size=params.size.compute_random_number(),
            energy=max(0, params.energy.compute_random_number()),
            energy_decay=params.energy_decay.compute_random_number(),
            position=position,
        )
        for position in clustered_positions
    ]


def init_animals(params: AnimalParams, amount: int) -> List[Animal]:
    """Initialises a list of animals in random positions using the specified parameters"""
    positions = [generate_random_position() for _ in range(amount)]
    return [
        Animal(
            food_size_factor=params.food_size_factor.compute_random_number(),
            search_algorithm=params.search_algorithm,
            size=params.size.compute_random_number(),
            speed=params.speed.compute_random_number(),
            vision=int(params.vision.compute_random_number()),
            food_reach_distance=params.food_reach_distance.compute_random_number(),
            energy_loss=params.energy_loss.compute_random_number(),
            cloning_size=params.cloning_size.compute_random_number(),
            random_position_generator=generate_random_position,
            position=position,
        )
        for position in positions
    ]


def clone_animals(
    animals: List[Animal],
    dispersion: int = 20,
    vision_dispersion: int = 20,
    colour_dispersion: int = 20,
    cloning_size_factor: float = 0.5,
):
    """Appends a number of clones the specified list of animals"""

    def _rand(x: float) -> float:  # pylint: disable=invalid-name
        return x + random.randint(0, dispersion)

    new_animals: List[Animal] = []
    for animal in animals:
        if animal.size > animal.cloning_size:
            new_animal = copy.deepcopy(animal)
            new_animal.size = max(1, (1 - cloning_size_factor) * animal.size)
            animal.size *= min(1, cloning_size_factor)

            new_animal.position = Coordinate(
                x=_rand(animal.position.x), y=_rand(animal.position.y)
            )
            r, g, b = animal.colour  # pylint: disable=invalid-name
            red_offset = random.randint(-colour_dispersion, colour_dispersion)
            new_animal.colour = (min(255, max(0, r + red_offset)), g, b)  # type: ignore
            new_animal.vision = max(
                1, animal.vision + random.randint(-vision_dispersion, vision_dispersion)
            )
            new_animal.cloning_size = max(0, animal.cloning_size + random.random())
            new_animal.speed = max(
                0.05, animal.speed * (1 + (+random.random() - 0.5) / 20)
            )
            new_animal.energy_loss = max(
                0, animal.energy_loss * (1 + (+random.random() - 0.5) / 20)
            )
            new_animal.target_position = None
            new_animals.append(new_animal)
    animals.extend(new_animals)


def main(params: RunnerParams, food_cloner: FoodCloner):
    """Main function"""
    # pylint: disable=no-member
    print(f"{SEED=}")
    random.seed(SEED)
    foods = init_foods(params.food, params.position_clusterer)
    animals = init_animals(params.animal, params.animal.initial_amount)
    search_algorithm = params.animal.search_algorithm
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size=tuple(SCREEN_SIZE))
    terminated = False

    plotting_data = PlotData()
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminated = True
                if event.key == pygame.K_RETURN:
                    foods = init_foods(params.food, params.position_clusterer)
                    animals = init_animals(params.animal, params.animal.initial_amount)

        search_algorithm.update()
        animals = [animal for animal in animals if not animal.dead]
        foods = [food for food in foods if not food.dead]
        food_cloner.clone(foods, SCREEN_SIZE)

        foods_dict: DefaultDict[Coordinate, List[Food]] = defaultdict(list)
        for food in foods:
            foods_dict[food.position].append(food)
        for animal in reversed(animals):
            animal.update(foods, foods_dict)
        for food in foods:
            food.update()
        clone_animals(
            animals,
            dispersion=ANIMAL_CLONE_DISPERSION,
            vision_dispersion=ANIMAL_VISION_DISPERSION,
            colour_dispersion=ANIMAL_COLOUR_DISPERSION,
            cloning_size_factor=ANIMAL_CLONING_SIZE_FACTOR,
        )

        if RANDOM_NEW_ANIMAL_CHANCE >= random.random():
            animals.extend(init_animals(params.animal, amount=1))

        screen.fill((0, 0, 0))
        for entity in animals + foods:  # type: ignore
            entity.draw(screen)
        pygame.display.flip()
        clock.tick(FRAMERATE)

        if not animals or not foods:
            break

        plotting_data.vision.append(statistics.mean(x.vision for x in animals))
        plotting_data.size.append(statistics.mean(x.size for x in animals))
        plotting_data.speed.append(statistics.mean(x.speed for x in animals))
        plotting_data.energy_loss.append(
            statistics.mean(x.energy_loss for x in animals)
        )
        plotting_data.food_energy.append(statistics.mean(x.energy for x in foods))
        plotting_data.food_amount.append(len(foods))
        plotting_data.animal_amount.append(len(animals))

    pygame.display.quit()
    plot_data(plotting_data, "output.png")


if __name__ == "__main__":
    main(
        params=RunnerParams(
            food=FoodParams(
                initial_amount=500,
                energy=Stat(average=10, standard_deviation=4, min=1),
                energy_decay=Stat(average=0.5),
            ),
            animal=AnimalParams(
                search_algorithm=SearchAlgorithm(max_entities_considered=2),
                initial_amount=50,
                vision=Stat(average=70, standard_deviation=10, min=1),
                energy_loss=Stat(
                    average=0.00007, standard_deviation=0.00001, min=0.00001
                ),
                cloning_size=Stat(average=25, standard_deviation=5),
                food_reach_distance=Stat(average=10, standard_deviation=2, min=1),
                speed=Stat(average=3, standard_deviation=0.5, min=0.3),
                food_size_factor=Stat(average=1),
            ),
            position_clusterer=SimplePositionClusterer(
                PositionBinner(100), SimplePositionLerper(0.1)
            ),
        ),
        food_cloner=FoodCloner(
            chance=0.03,
            size_dispersion=0.2,
            energy_dispersion=0.2,
            max_dispersion=50,
            max_length=500,
            max_size=12,
            min_size=3,
        ),
    )
