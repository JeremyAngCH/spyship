import pygame

"""
SpriteSheet Class
-----------------
Spritesheet is an image that consists of several smaller images/sprites
placing next to each other. These smaller images/sprites are usually
a sequence of animation frames.
This simple class creates a new sprite frame out of spritesheet.
For example, if a spritesheet has 5 animation frames, we can use
this class to create 5 sprite frames so that these frames can be drawn
individually on screen.
"""


class SpriteSheet:

    def __init__(self, filename):
        self.__spriteSheet = pygame.image.load(filename).convert_alpha()

    def getFrame(self, x, y, width, height):
        # Create a new surface for an animation frame
        frame = pygame.Surface([width, height], pygame.SRCALPHA, 32). \
                convert_alpha()
        # Copy the sprite from the spritesheet to the new surface
        frame.blit(self.__spriteSheet, (0, 0), (x, y, width, height))
        return frame
