import pygame
import random
from gameobj import GameObj

"""
Asteroid Class
--------------
Flying Rocks/stones in the space background.
"""


class Asteroid(GameObj):
    # 2 types of asteroid - Grey and brown color
    GREY = 1
    BROWN = 2

    def __init__(self, x=0, y=0, speedX=-0.5, col=GREY):
        super(Asteroid, self).__init__()
        # speedX is always a negative number because asteroid always
        # move from right to left
        self.dx = speedX
        self.__img = pygame.image.load("res/img/asteroid%02d.png" % col). \
            convert_alpha()
        scaleFact = random.uniform(1.5, 3)
        # Randomly scale down the asteroid image
        self.__img = pygame.transform.scale(self.__img,
                                            (int(self.__img.get_rect().width /
                                                 scaleFact),
                                             int(self.__img.get_rect().height /
                                                 scaleFact)))
        # Rotate the asteroid image with random angle
        self.__img = pygame.transform.rotate(self.__img,
                                             random.uniform(0, 360))
        self.rect = self.__img.get_rect()
        self.setPos(x, y)

    def setPos(self, x, y):
        self.rect.centerx = int(x)
        self.rect.centery = int(y)
        super(Asteroid, self).setPos(x, y)

    def update(self):
        self.setPos(self.x + self.dx, self.y)

    def render(self, surf):
        surf.blit(self.__img, (self.rect.x, self.rect.y))

    def isExpired(self):
        # Mark the object as 'expired' if it moves passed the left edge
        # of the screen
        return (self.rect.right < 0)

    def getRect(self):
        return None
