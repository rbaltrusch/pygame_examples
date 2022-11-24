# -*- coding: utf-8 -*-
"""Contains algorithms used to traverse 2d space using linear interpolation
and position binning.
"""
import statistics
from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Protocol
from typing import Tuple

import pygame
from src.coordinate import Coordinate

# pylint: disable=c-extension-no-member
# pylint: disable=too-few-public-methods


class Entity(Protocol):
    """Entity interface"""

    position: Coordinate

    def draw(self, screen: pygame.surface.Surface):
        """Draws the entity on the screen"""
        ...


class PositionLerper(Protocol):
    """Interface for a position linear interpolator"""

    def lerp(self, position1: Coordinate, position2: Coordinate) -> Coordinate:
        """Returns a position between the two positions specified"""
        ...


class PositionClusterer(Protocol):
    """Interface for a position clusterer"""

    def cluster_positions(self, positions: Iterable[Coordinate]) -> List[Coordinate]:
        """Forms clusters using the specified positions and returns the resulting positions"""
        ...


@dataclass
class SimplePositionLerper:
    """Linearly interpolates between two points based on a factor betwee 0 and 1"""

    factor: float

    def lerp(self, position1: Coordinate, position2: Coordinate) -> Coordinate:
        """Returns a point between the two specified points"""

        def _lerp(x: float, y: float) -> float:  # pylint: disable=invalid-name
            return x * (1 - self.factor) + y * self.factor

        return Coordinate(
            x=_lerp(position1.x, position2.x), y=_lerp(position1.y, position2.y)
        )


@dataclass
class PositionBinner:
    """Groups positions into bins of positions close to each other"""

    bin_resolution: int

    def __post_init__(self):
        self.bin_resolution = int(self.bin_resolution)

    def compute_position_bins(
        self, positions: Iterable[Coordinate]
    ) -> DefaultDict[Tuple[int, int], List[Coordinate]]:
        """Groups the specified positions into bins of close positions, where the size
        of each bin (which positions are deemed close to each other) is specified by this
        PositionBinner's bin_resolution.
        """
        positions_bins = defaultdict(list)  # type: ignore
        for position in positions:
            positions_bins[self.floor_position(position)].append(position)  # type: ignore
        return positions_bins  # type: ignore

    def floor_position(self, position: Coordinate) -> Tuple[int, int]:
        """Returns the bin position tuple of ints that can be used to look up the
        specified position from the calculated position bins.
        """
        bin_resolution = self.bin_resolution
        return (
            position.x // bin_resolution * bin_resolution,
            position.y // bin_resolution * bin_resolution,
        )  # type: ignore


def average_positions(positions: Iterable[Coordinate]) -> Coordinate:
    """Returns the average point in the specified list of points"""
    x, y = zip(*positions)  # pylint: disable=invalid-name
    return Coordinate(x=statistics.mean(x), y=statistics.mean(y))


@dataclass
class SimplePositionClusterer:
    """Clusters positions using a position binner and position lerper"""

    position_binner: PositionBinner
    lerper: PositionLerper

    def cluster_positions(self, positions: Iterable[Coordinate]) -> List[Coordinate]:
        """Clusters the specified positions by binning them, then using linear interpolation
        to move positions in the same bin closer to each other.
        """
        bin_averages = {
            k: average_positions(v)
            for k, v in self.position_binner.compute_position_bins(positions).items()
        }
        return [
            self.lerper.lerp(
                pos, bin_averages[self.position_binner.floor_position(pos)]
            )
            for pos in positions
        ]


@dataclass
class CompositePositionClusterer:
    """Allows position clusterer chains, while maintaining the same PositionClusterer interface."""

    clusterers: List[PositionClusterer]

    def cluster_positions(self, positions: Iterable[Coordinate]) -> List[Coordinate]:
        """Forms clusters using the specified positions and returns the resulting positions"""
        for clusterer in self.clusterers:
            positions = clusterer.cluster_positions(positions)
        return positions  # type: ignore


@dataclass
class SearchAlgorithm:
    """Simple search algorithm to find the closest target from a list of entities"""

    binner_type = PositionBinner

    def determine_target_position(
        self, entity: Entity, entities: List[Entity], distance: int
    ) -> Optional[Coordinate]:
        """Uses a position binner (using the specified distance as the bin_resolution)
        to find the closest of the specified entities to the specified entity. If none
        can be found in that position bin, return None, else return the closest entity in the bin.
        """
        binner = self.binner_type(bin_resolution=distance)
        position_bins = binner.compute_position_bins(
            positions=[x.position for x in entities]
        )
        bin_ = position_bins.get(binner.floor_position(entity.position))
        return min(bin_, key=entity.position.compute_distance) if bin_ else None
