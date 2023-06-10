[![Pylint](https://github.com/rbaltrusch/pygame_examples/actions/workflows/pylint.yml/badge.svg)](https://github.com/rbaltrusch/pygame_examples/actions/workflows/pylint.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)

# Pygame examples

A repository for short pygame drafts, examples, tutorials and more!

Currently, this repository contains a draft lighting system, a particle system, a networked game, a hexogonal tile system, a cloth simulation and other cool pygame examples.

![Gif of the particle effects](https://github.com/rbaltrusch/pygame_examples/blob/master/media/particle_effects.gif?raw=true "Gif of the particle effects")
![Gif of the lighting system](https://github.com/rbaltrusch/pygame_examples/blob/master/media/lighting_system.gif?raw=true "Gif of the lighting system")
![Gif of the hexagonal tile map](media/hexagons.gif?raw=true "Gif of the hexagonal tile map")
![Gif of a red light source](media/red_light.gif?raw=true "Gif of a red light source")
![Gif of an evolution simulation](media/evolution_sim.gif?raw=true "Gif of an evolution simulation")
![Gif of the cloth simulation](media/cloth_sim2.gif?raw=true "Gif of the cloth simulation")

## Getting started

To get a copy of this repository, simply open up git bash in an empty folder and use the command:

    $ git clone https://github.com/rbaltrusch/pygame_examples

Dependencies can be installed using the requirements.txt as below:

```
pip install -r requirements.txt
```

To run some of the examples, navigate to the respective folder in the code folder, then run main.py.

## Contents

This repository contains the following small pygame examples:
- [Particle system](code/particle_system): contains a simple, but effective, particle system implementation.
- [Evolution simulation](code/evolution_simulation): contains a simple simulation of evolving animals hunting for food.
- [Cloth simulation](code/cloth_simulation): contains a cloth simulation with custom physics.
- [Game console](code/game_console): contains a minimal implementation of an in-game console.
- [Animation testing tool](code/animator): can be used to test out animations. Contains a fully featured in-game console with a decoupled and flexible design.
- [Networked game](code/networked_game): contains a minimal implementation of a networked game, featuring one external server and two separate clients, communicating with each other through the server.
- [Dynamic lighting](code/simple_lighting): contains a small draft implementation for dynamic in-game lighting.
- [Hexagonal grid](code/hexagonal_tiles): contains an implementation of a hexagonal grid, including collision handling.
- [Tidy event queue](code/tidy_event_queue): contains an exercise in decoupling complex pygame event handling constructs into separate parts.
- [Async events](code/async_events): contains an example implementation for an asynchronous event handler (useful for writing linear-looking code for events with execution spread out over multiple game cycles).
- [Squish and stretch](code/squish_and_stretch): contains an example implementation of squishing and stretching an image.
- [Timed events](code/timed_events): contains an implementation of callbacks executed after a specified delay. Not pygame-specific.
- [Random starry sky](code/random_screen_animation): generates a random starry sky.

## Contributions

To contribute to this repository, please read the [contribution guidelines](CONTRIBUTING.md).

## Python

Written in Python 3.8.3.

## License

This repository is open-source software available under the [MIT license](https://github.com/rbaltrusch/pygame_examples/blob/master/LICENSE).

## Contact

Please raise an issue for code changes. To reach out, please send an email to richard@baltrusch.net.
