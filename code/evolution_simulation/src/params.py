# -*- coding: utf-8 -*-
"""Contains parameters for the initialization of the simulation"""
import random
from dataclasses import dataclass

try:
    import numpy
except ImportError:
    print(
        "Could not import numpy, substituting normal distribution with flat distribution"
    )
    numpy = None

from src.search import SearchAlgorithmInterface, PositionClusterer


@dataclass
class Stat:
    """Encapsulates parameters to draw random values from a normal distribution"""

    average: float
    standard_deviation: float = 0
    min: float = 0

    def compute_random_number(self) -> float:
        """Returns a random number taken from the a normal distribution
        defined by this Stat's average and standard deviation.
        """
        number: float = (
            numpy.random.normal(self.average, self.standard_deviation)  # type: ignore
            if numpy is not None
            else random.random() * self.average
        )
        return max(self.min, number)


@dataclass(frozen=True)
class FoodParams:
    """Simulation init parameters related to food"""

    initial_amount: int = 50
    size: Stat = Stat(average=5, standard_deviation=1)
    energy: Stat = Stat(average=5, standard_deviation=1)
    energy_decay: Stat = Stat(average=1)
    screen_offset: int = 50


@dataclass(frozen=True)
class AnimalParams:  # pylint: disable=too-many-instance-attributes
    """Simulation init parameters related to animals"""

    search_algorithm: SearchAlgorithmInterface
    initial_amount: int = 10
    size: Stat = Stat(average=10, standard_deviation=3)
    speed: Stat = Stat(average=2, standard_deviation=0.5)
    vision: Stat = Stat(average=10, standard_deviation=1, min=1)
    food_reach_distance: Stat = Stat(average=10, standard_deviation=1)
    energy_loss: Stat = Stat(average=1)
    food_size_factor: Stat = Stat(average=1)
    cloning_size: Stat = Stat(average=20, standard_deviation=1)


@dataclass(frozen=True)
class RunnerParams:
    """Simulation init parameters"""

    food: FoodParams
    animal: AnimalParams
    position_clusterer: PositionClusterer
