# -*- coding: utf-8 -*-
"""
Cloth simulation with custom physics implementation:
    Force of gravity, air resistance, elastic restoration force

Controls:
    Pick up and move a node by dragging it with the mouse
    Press A while dragging a node to toggle its affixed status
    Press Q to decrease wind force / increase wind to the left
    Press W to increase wind force / increase wind to the right
    Press R to respawn cloth nodes
    Press Escape to exit
"""

# pylint: disable=no-member
# pylint: disable=invalid-name
# pylint: disable=c-extension-no-member

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional
import pygame


POLYGON_COLOUR = (50, 50, 50)
LINE_COLOUR = (255, 255, 255)
FPS = 500
TICK = 0.01
MIN_MASS = 0.01
NODE_RADIUS = 3
NODE_MASS = 400
GRAVITY = 10_000
MIN_FORCE_THRESHOLD = 0
AIR_FRICTION_COEFFICIENT = 500
ELASTICITY = 1_000_000


def calculate_acceleration(force: float, speed: float, mass: float) -> float:
    """
    Calculates acceleration from the specified force and mass,
    factoring in air resistance drag force calculated from the specified (current) speed.
    """
    air_resistance = min(abs(force), calculate_air_resistance_force(speed))
    drag_direction = 1 if speed > 0 else 0
    total_force = force - air_resistance * drag_direction
    if abs(total_force) < MIN_FORCE_THRESHOLD:
        total_force = 0
    return total_force / max(mass, MIN_MASS)


def calculate_air_resistance_force(speed: float) -> float:
    """
    Returns the air resistance (drag force) based on the specified speed
    Note: this equation is a simplification of the actual equation:
    F = (1/2) p v² C A, representing (1/2) p C A as AIR_FRICTION_COEFFICIENT
    source: https://en.wikipedia.org/wiki/Drag_(physics)#The_drag_equation
    """
    return AIR_FRICTION_COEFFICIENT * speed**2


@dataclass
class NodeConnection:
    """Encapsulates a node between two nodes to handle elastic restoration force physics"""

    start: Node
    end: Node
    elasticity: float = 0

    def set_elastic_restoring_forces(self) -> None:
        """Calculates symmetric elastic forces in x and y directions using Hook's law
        F = k x where k is the elastic constant (here the elasticity of the connection)
        and x the displacement from rest position.
        The calculated force is split evenly between both nodes of the connection.
        """
        self._set_elastic_restoring_y_forces()
        self._set_elastic_restoring_x_forces()

    def _set_elastic_restoring_y_forces(self) -> None:
        length = self.start.y - self.end.y
        force = length * self.elasticity / 2
        self.end.elastic_restoring_y_force += force
        self.start.elastic_restoring_y_force -= force

    def _set_elastic_restoring_x_forces(self) -> None:
        length = self.start.x - self.end.x
        force = length * self.elasticity / 2
        self.end.elastic_restoring_x_force += force
        self.start.elastic_restoring_x_force -= force


@dataclass
class Node:
    """Node class with custom physics implementation"""

    mass: float
    x: float = 0
    y: float = 0
    speed_x: float = 0
    speed_y: float = 0
    previous_node_y_connection: Optional[NodeConnection] = None
    previous_node_x_connection: Optional[NodeConnection] = None
    affixed: bool = False

    def __post_init__(self):
        self.elastic_restoring_y_force: float = 0
        self.elastic_restoring_x_force: float = 0

    def reset(self):
        """Resets the node's elastic forces"""
        self.elastic_restoring_y_force = 0
        self.elastic_restoring_x_force = 0

    def update(self):
        """Updates the node force, speed and position"""
        if self.affixed:
            return
        self.speed_y += self._calculate_vertical_acceleration() * TICK
        self.speed_x += self._calculate_horizontal_acceleration() * TICK
        self.y += self.speed_y * TICK
        self.x += self.speed_x * TICK

    def render(self, screen: pygame.surface.Surface) -> None:
        """Renders the node using a four-sided polygon"""
        if not self.previous_node_x_connection or not self.previous_node_y_connection:
            return

        points = [
            self.previous_node_x_connection.start.position,
            self.position,
            self.previous_node_y_connection.start.position,
        ]
        conn = self.previous_node_x_connection.start.previous_node_y_connection
        if conn:
            points.append(conn.start.position)
        pygame.draw.polygon(screen, POLYGON_COLOUR, points)
        pygame.draw.polygon(screen, LINE_COLOUR, points, width=1)

    def _calculate_vertical_acceleration(self) -> float:
        """
        Calculates the force of gravity using Newton's second law of motion:
        F = m a, where m is the node mass and a the acceleration due to gravity.
        """
        force = self.mass * GRAVITY + self.elastic_restoring_y_force
        return calculate_acceleration(force, self.speed_y, self.mass)

    def _calculate_horizontal_acceleration(self) -> float:
        force = self.elastic_restoring_x_force
        return calculate_acceleration(force, self.speed_x, self.mass)

    def set_elastic_restoring_force(self) -> None:
        """
        Sets vertical elastic forces.
        Crashes for some reason when also setting horizontal forces?
        """
        if self.previous_node_y_connection is not None:
            self.previous_node_y_connection.set_elastic_restoring_forces()

    @property
    def position(self):
        """The position of the node"""
        return (self.x, self.y)


def connect_nodes(nodes: List[Node], elasticity: float) -> None:
    """Connects all specified nodes into"""
    if len(nodes) < 2:
        return
    nodes[0].affixed = True
    for previous_node, node in zip(nodes, nodes[1:]):
        node.previous_node_y_connection = NodeConnection(
            start=previous_node, end=node, elasticity=elasticity
        )


def connect_ropes(ropes: List[List[Node]], elasticity: float) -> None:
    """Connects each "rope" (vertically-connected nodes) horizontally to form a connected grid"""
    if len(ropes) < 2:
        return
    for nodes in zip(*ropes):
        node: Node
        for previous_node, node in zip(nodes, nodes[1:]):
            node.previous_node_x_connection = NodeConnection(
                start=previous_node, end=node, elasticity=elasticity
            )


def update_nodes(nodes: List[Node], wind: float) -> None:
    """Updates node physics by calculating node forces, speeds and positions"""
    for node in nodes:
        node.reset()
    for node in nodes:
        node.elastic_restoring_x_force = wind
    for node in nodes:
        node.set_elastic_restoring_force()
    for node in nodes:
        node.update()


def init_cloth_nodes() -> List[Node]:
    """Initializes a grid of interconnected nodes to simulate cloth, then returns all  nodes"""
    ropes: List[List[Node]] = []
    for x in range(200, 600, 50):
        nodes = [Node(x=x, y=50, mass=NODE_MASS) for _ in range(10)]
        connect_nodes(nodes, elasticity=ELASTICITY)
        ropes.append(nodes)
    connect_ropes(ropes, elasticity=ELASTICITY * 100)
    return [node for rope in ropes for node in rope]


def main():
    """Main function"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    nodes = init_cloth_nodes()

    wind: float = 0
    terminated = False
    selected_node: Optional[Node] = None
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected_node = min(
                    nodes, key=lambda x: math.dist(pygame.mouse.get_pos(), x.position)
                )
            elif event.type == pygame.MOUSEBUTTONUP:
                selected_node = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminated = True
                if event.key == pygame.K_r:
                    nodes = init_cloth_nodes()
                elif event.key == pygame.K_q:
                    wind -= 100_000
                elif event.key == pygame.K_w:
                    wind += 100_000
                elif event.key == pygame.K_a and selected_node:
                    selected_node.affixed = not selected_node.affixed
                    selected_node = None

        if selected_node is not None:
            selected_node.x, selected_node.y = pygame.mouse.get_pos()

        print(f"{wind=}")
        update_nodes(nodes, wind)
        screen.fill((0, 0, 0))
        for node in nodes:
            node.render(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
