# -*- coding: utf-8 -*-
"""
A light source experiment based on emitting light particles from a source point.

Use W and S keys to increase and decrease the particle speed
(and thus the perceived brightness of the light source) during the simulation.

@author: Korean_Crimson
"""
# pylint: disable=no-member
import random
from dataclasses import dataclass
from typing import List
from typing import Tuple

import pygame


WIDTH = 800
HEIGHT = 600
ENERGY_DECAY = 0.05
MIN_ENERGY = 0.05
SPEED_SCALING = 5
COLLISION_REDUCTION_FACTOR = 0.2
MAX_RADIUS_INCREASE = 7  # this defines how chunky a particle will look!


def saturate(value, min_val=0, max_val=255):
    """Saturates a number between the provided min and max values"""
    return min(max(value, min_val), max_val)


@dataclass
class LightParticle:
    """Light particle class."""

    energy: float
    position: Tuple[float]
    speed: Tuple[float]
    colour: Tuple[float]
    max_radius_increase: int = MAX_RADIUS_INCREASE

    def update(self):
        """Updates the particle position, energy, colour and handles collisions"""
        pos_x, pos_y = self.position
        x, y = self.speed  # pylint: disable=invalid-name
        self.position = (pos_x + x * SPEED_SCALING, pos_y + y * SPEED_SCALING)
        self.energy *= 1 - ENERGY_DECAY
        self.update_colour()
        self.update_collisions()

    def update_colour(self):
        """Updates the colour of the light particle by removing some red and
        adding some green, effectively shifting the colour further towards orange/yellow.
        """
        # pylint: disable=invalid-name
        r, g, b, *a = self.colour
        self.colour = (
            int(saturate(r - self.energy * 0.1)),
            int(saturate(g + self.energy * 0.01)),
            b,
            *a,
        )

    def update_collisions(self):
        """Collisions with the screen edges decrease the particles energy and change
        the angle at which it travels."""
        # pylint: disable=invalid-name
        x, y = self.position
        speed_x, speed_y = self.speed
        if not 0 <= x <= WIDTH:
            self.speed = (-speed_x, speed_y)
            self.energy *= COLLISION_REDUCTION_FACTOR
        if not 0 <= y <= HEIGHT:
            self.speed = (speed_x, -speed_y)
            self.energy *= COLLISION_REDUCTION_FACTOR

    def render(self, screen):
        """Renders the particle on the screen"""
        # render a number of circles around the main particle circle
        max_increase = self.max_radius_increase
        max_radius = self.radius + max_increase
        surf = pygame.Surface((max_radius * 2, max_radius * 2))
        for i in range(max_increase, 0, -2):
            colour = tuple(
                saturate(x * (max_increase - i) / (max_increase / 2))
                for x in self.colour
            )
            radius = self.radius + i
            pygame.draw.circle(surf, colour, (radius, radius), radius)
        screen.blit(surf, self.position, special_flags=pygame.BLEND_RGBA_ADD)

        pygame.draw.circle(screen, self.colour, self.position, self.radius)

    @property
    def radius(self) -> float:
        """The radius of the particle when rendered"""
        return self.energy

    @property
    def expired(self) -> bool:
        """The expired status of the particle, True if energy is less than zero"""
        return self.energy <= MIN_ENERGY


@dataclass
class LightSource:
    """Light source, which emits light particles each tick"""

    spawn: int = 1
    energy: float = 10
    position: Tuple[int, int] = (0, 0)
    colour: Tuple[int, int, int] = (255, 255, 255)

    def __post_init__(self):
        self.particles: List[LightParticle] = []

    def update(self):
        """Updates all particles, removes expired particles and spawns new ones"""
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if not p.expired]
        self.spawn_particles()

    def spawn_particles(self):
        """Spawns a number of particles, depending on the light source energy and spawn
        rate. Each particle will get a unit vector (magnitude 1) that specifies the angle
        at which it is emitted, as well as a slight colour variation of the light source colour,
        and an energy between 0% and 200% of the light source energy.
        """
        energy = self.energy / self.spawn
        for _ in range(self.spawn):
            vel_x = random.randint(-10000, 10000) / 10000
            vel_y = (1 - abs(vel_x)) * random.choice([1, -1])
            speed = (vel_x, vel_y)
            colour = tuple(saturate(x + random.randint(-10, 10)) for x in self.colour)
            self.particles.append(
                LightParticle(
                    energy * random.randint(0, 200) / 100, self.position, speed, colour
                )
            )

    def render(self, screen):
        """Renders the light source on the screen"""
        for particle in self.particles:
            particle.render(screen)


def main():
    """Main function"""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    light_source = LightSource(
        spawn=25, energy=30, position=(200, 200), colour=(255, 50, 20, 20)
    )

    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            if event.type == pygame.KEYDOWN:
                global SPEED_SCALING
                if event.key == pygame.K_s:
                    SPEED_SCALING -= 1
                if event.key == pygame.K_w:
                    SPEED_SCALING += 1

        light_source.update()
        light_source.position = pygame.mouse.get_pos()
        screen.fill(
            (5, 5, 5), special_flags=pygame.BLEND_RGBA_SUB
        )  # dim colours over time
        light_source.render(screen)
        pygame.display.flip()
        clock.tick(50)

    pygame.display.quit()


if __name__ == "__main__":
    main()
