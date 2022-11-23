# -*- coding: utf-8 -*-
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class Coordinate:

    x: float
    y: float

    def __iter__(self):
        yield self.x
        yield self.y

    def __hash__(self):
        return hash(tuple(self))

    def compute_distance(self, coordinate: Coordinate) -> float:
        return math.dist(tuple(self), tuple(coordinate))
