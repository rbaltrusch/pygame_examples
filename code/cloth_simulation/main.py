# -*- coding: utf-8 -*-
""""""

# pylint: disable=no-member
# pylint: disable=invalid-name
# pylint: disable=c-extension-no-member

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional, Tuple
import pygame

MIN_MASS = 0.01
NODE_COLOUR = (255, 255, 255)
LINE_COLOUR = (255, 255, 255)
NODE_RADIUS = 10
MASS_PER_LENGTH = 100
GRAVITY = 10_000
AIR_FRICTION_COEFFICIENT = 500
FPS = 100
TICK = 0.02


@dataclass
class NodeConnection:
    node: Node
    nominal_length: float
    mass_per_length: float
    elasticity: float = 0

    def __post_init__(self):
        self.length: float = self.nominal_length

    def render(self, screen: pygame.surface.Surface, end_position: Tuple[float, float]):
        pygame.draw.line(screen, LINE_COLOUR, self.node.position, end_position)

    # def calculate_vertical_force(self) -> float:
    #     return self.node.calculate_vertical_force()

    def calculate_elastic_restoring_force(self, node: Node) -> float:
        direction = 1 if self.node.y < node.y else -1
        length = math.dist(self.node.position, node.position)
        # print(
        #     "len",
        #     length,
        #     self.node.position,
        #     node.position,
        #     (self.nominal_length - length) * self.elasticity * direction,
        # )
        return (self.nominal_length - length) * self.elasticity * direction

    @property
    def mass(self) -> float:
        return self.mass_per_length * self.nominal_length

    @property
    def total_mass(self) -> float:
        mass = self.mass
        if self.node.previous_node_connection is None:
            return mass
        return mass + self.node.previous_node_connection.total_mass


@dataclass
class Node:
    x: float = 0
    y: float = 0
    speed_x: float = 0
    speed_y: float = 0
    previous_node_connection: Optional[NodeConnection] = None
    affixed: bool = False

    def update(self):
        if self.affixed:
            return
        self.speed_y += self.calculate_vertical_acceleration() * TICK
        self.y += self.speed_y * TICK

    def render(self, screen: pygame.surface.Surface) -> None:
        if self.previous_node_connection:
            self.previous_node_connection.render(screen, self.position)
        pygame.draw.circle(screen, NODE_COLOUR, self.position, NODE_RADIUS)

    def calculate_vertical_acceleration(self) -> float:
        if self.previous_node_connection is None:
            return 0
        force = self.calculate_vertical_force()
        air_resistance = min(abs(force), self.calculate_air_resistance_force())
        drag_direction = 1 if self.speed_y > 0 else 0
        total_force = force - air_resistance * drag_direction
        return total_force / max(self.previous_node_connection.mass, MIN_MASS)

    def calculate_vertical_force(self) -> float:
        segment_force = self.calculate_segment_force()
        return segment_force

    def calculate_segment_force(self) -> float:
        if self.previous_node_connection is None:
            return 0
        return (
            self.previous_node_connection.mass * GRAVITY
            + self.previous_node_connection.calculate_elastic_restoring_force(self)
        )

    def calculate_air_resistance_force(self) -> float:
        return AIR_FRICTION_COEFFICIENT * self.speed_y**2

    @property
    def position(self):
        return (self.x, self.y)


def connect_nodes(nodes: List[Node], length: float, elasticity: float) -> None:
    if len(nodes) < 2:
        return
    # nodes[0].affixed = True
    for previous_node, node in zip(nodes, nodes[1:]):
        node.previous_node_connection = NodeConnection(
            previous_node,
            nominal_length=length,
            mass_per_length=MASS_PER_LENGTH,
            elasticity=elasticity,
        )
        node.y = previous_node.y + length * 0.8


def main():
    """Main function"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    nodes = [Node(x=200, y=50) for _ in range(8)]
    connect_nodes(nodes, length=1, elasticity=20000)

    terminated = False
    selected_node: Optional[Node] = None
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                distances = [math.dist(x.position, mouse_pos) for x in nodes]
                dist, node = min(zip(distances, nodes))
                if dist < NODE_RADIUS:
                    selected_node = node
            elif event.type == pygame.MOUSEBUTTONUP:
                selected_node = None

        if selected_node is not None:
            selected_node.y = pygame.mouse.get_pos()[1]
        for node in nodes:
            node.update()
        screen.fill((0, 0, 0))
        for node in nodes:
            node.render(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
