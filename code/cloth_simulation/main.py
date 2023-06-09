# -*- coding: utf-8 -*-
""""""

# pylint: disable=no-member
# pylint: disable=invalid-name
# pylint: disable=c-extension-no-member

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional
import pygame

MIN_MASS = 0.01
NODE_COLOUR = (255, 255, 255)
LINE_COLOUR = (255, 255, 255)
NODE_RADIUS = 3
NODE_MASS = 100
GRAVITY = 10_000
MIN_FORCE_THRESHOLD = 0
AIR_FRICTION_COEFFICIENT = 500
FPS = 200
TICK = 0.02
NODE_SELECT_RADIUS = 20


@dataclass
class NodeConnection:
    start: Node
    end: Node
    nominal_length: float
    elasticity: float = 0

    def __post_init__(self):
        self.length: float = self.nominal_length

    def render(self, screen: pygame.surface.Surface):
        pygame.draw.line(screen, LINE_COLOUR, self.start.position, self.end.position)

    def set_elastic_restoring_forces(self) -> None:
        direction = 1 if self.start.y < self.end.y else -1
        length = math.dist(self.start.position, self.end.position)
        force = (self.nominal_length - length) * self.elasticity * direction
        self.end.elastic_restoring_force += force / 2
        self.start.elastic_restoring_force -= force / 2


@dataclass
class Node:
    mass: float
    x: float = 0
    y: float = 0
    speed_x: float = 0
    speed_y: float = 0
    previous_node_connection: Optional[NodeConnection] = None
    affixed: bool = False

    def __post_init__(self):
        self.elastic_restoring_force: float = 0

    def reset(self):
        self.elastic_restoring_force = 0

    def update(self):
        if self.affixed:
            return
        self.speed_y += self.calculate_vertical_acceleration() * TICK
        self.y += self.speed_y * TICK

    def render(self, screen: pygame.surface.Surface) -> None:
        if self.previous_node_connection:
            self.previous_node_connection.render(screen)
        pygame.draw.circle(screen, NODE_COLOUR, self.position, NODE_RADIUS)

    def calculate_vertical_acceleration(self) -> float:
        force = self.calculate_vertical_force()
        air_resistance = min(abs(force), self.calculate_air_resistance_force())
        drag_direction = 1 if self.speed_y > 0 else 0
        total_force = force - air_resistance * drag_direction
        if abs(total_force) < MIN_FORCE_THRESHOLD:
            total_force = 0
        return total_force / max(self.mass, MIN_MASS)

    def set_elastic_restoring_force(self) -> None:
        if self.previous_node_connection is not None:
            self.previous_node_connection.set_elastic_restoring_forces()

    def calculate_vertical_force(self) -> float:
        force_of_gravity = self.mass * GRAVITY
        return force_of_gravity + self.elastic_restoring_force

    def calculate_air_resistance_force(self) -> float:
        return AIR_FRICTION_COEFFICIENT * self.speed_y**2

    @property
    def position(self):
        return (self.x, self.y)


def connect_nodes(nodes: List[Node], elasticity: float) -> None:
    if len(nodes) < 2:
        return
    nodes[0].affixed = True
    for previous_node, node in zip(nodes, nodes[1:]):
        node.previous_node_connection = NodeConnection(
            start=previous_node,
            end=node,
            nominal_length=0,
            elasticity=elasticity,
        )


def update_nodes(nodes: List[Node]) -> None:
    for node in nodes:
        node.reset()
    for node in nodes:
        node.set_elastic_restoring_force()
    for node in nodes:
        node.update()


def main():
    """Main function"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    nodes = [Node(x=200, y=50, mass=NODE_MASS) for _ in range(10)]
    connect_nodes(nodes, elasticity=200_000)

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
                if dist < max(NODE_RADIUS, NODE_SELECT_RADIUS):
                    selected_node = node
                else:
                    node.previous_node_connection = None
            elif event.type == pygame.MOUSEBUTTONUP:
                selected_node = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    nodes = [Node(x=200, y=50, mass=NODE_MASS) for _ in range(10)]
                    connect_nodes(nodes, length=0, elasticity=200_000)

        if selected_node is not None:
            selected_node.y = pygame.mouse.get_pos()[1]

        update_nodes(nodes)
        screen.fill((0, 0, 0))
        for node in nodes:
            node.render(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
