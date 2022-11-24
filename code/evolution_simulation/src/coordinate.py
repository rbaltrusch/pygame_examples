# -*- coding: utf-8 -*-
"""Coordinates module"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class Coordinate:
    """Coordinate point class"""

    x: float  # pylint: disable=invalid-name
    y: float  # pylint: disable=invalid-name

    def __iter__(self):
        yield self.x
        yield self.y

    def __hash__(self):
        return hash(tuple(self))

    def compute_distance(self, coordinate: Coordinate) -> float:
        """Returns the distance from this point to the specified point"""
        return math.dist(tuple(self), tuple(coordinate))
