# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 15:03:15 2021

Press F1 to start animation
Press F2 to stop animation
Press ENTER to open

Supports the following commands:
    /folder x          read in folder for animation frames
    /fps x             set speed of animation
    /position x x      set animation position
    /alpha x x x       set the specified colour to transparent
    /repeat [on|off]   set animation repeat on or off


@author: richa
"""
# pylint: disable=no-member
import init
import pygame

FPS = 12


def set_fps(value):
    """Sets the global fps value. Event callback for SET_FPS"""
    global FPS  # pylint: disable=global-statement
    FPS = value


def render(screen, entities):
    """Renders the entities on the screen"""
    screen.fill((255, 255, 255))
    for entity in entities:
        entity.render(screen)
    pygame.display.flip()


def main():
    """Main function"""
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    animation, event_queue, console = init.init()
    event_queue.subscribe("SET_FPS", set_fps)

    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                console.toggle_activate()
                if not console.active:
                    console.execute()
            elif event.type == pygame.TEXTINPUT and console.active:
                console.add_text(event.text)
            elif (
                event.type == pygame.KEYUP
                and event.key == pygame.K_BACKSPACE
                and console.active
            ):
                console.remove_last_char()
            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                console.errored = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_F1:
                animation.active = True
                animation.counter = 0
            elif event.type == pygame.KEYUP and event.key == pygame.K_F2:
                animation.active = False

        event_queue.update()
        render(screen, entities=[animation, console])
        clock.tick(FPS)

    pygame.display.quit()


if __name__ == "__main__":
    main()
