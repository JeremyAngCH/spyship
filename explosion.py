import pygame
import random
from spritesheet import SpriteSheet
from gameobj import GameObj

EXPLOSION_TYPE_NUM = 2
expsFrames = [
                [
                    (0, 0, 56, 50),
                    (57, 0, 56, 50),
                    (114, 0, 56, 50),
                    (171, 0, 56, 50),
                    (228, 0, 56, 50),
                    (285, 0, 56, 50),
                    (342, 0, 56, 50),
                    (399, 0, 56, 50),
                    (456, 0, 56, 50),
                    (513, 0, 56, 50)
                ],
                [
                    (0, 0, 27, 27),
                    (28, 0, 27, 27),
                    (56, 0, 27, 27),
                    (84, 0, 27, 27)
                ]
            ]


"""
Explosion Class
---------------
Explosion animation for spaceship.
"""


class Explosion(GameObj):

    EXPLOSION01_TYPE = 0
    EXPLOSION02_TYPE = 1

    spriteSheet = [None] * EXPLOSION_TYPE_NUM
    imgs = [[] for n in range(EXPLOSION_TYPE_NUM)]

    def __init__(self, x, y, objType):
        super(Explosion, self).__init__(x, y, False)
        self.__objType = objType
        self.__rect = None
        for i in range(EXPLOSION_TYPE_NUM):
            if not Explosion.spriteSheet[i]:
                Explosion.spriteSheet[i] = SpriteSheet(
                                                "res/img/explosion%02d.png" %
                                                (i + 1))

        if not Explosion.imgs[objType]:
            for frames in expsFrames[objType]:
                Explosion.imgs[objType].append(Explosion.spriteSheet[objType].
                                               getFrame(*frames))
        self.__animTimer = pygame.time.get_ticks()
        # Animate the explosion in slightly different speed so that
        # if multiple explosions are displayed on screen, they
        # looked slightly different.
        self.__explosionFrameDelay = 40 + (random.randint(0, 8) * 5)
        self.reset()

    def reset(self):
        self.__curFrameIndex = 0
        self.state = Explosion.ALIVE
        self.setFrame(0)

    def setFrame(self, frameIndex):
        self.__img = (Explosion.imgs[self.__objType])[frameIndex]
        self.__rect = self.__img.get_rect()
        self.setPos(self.x, self.y)

    def setPos(self, x, y):
        self.__rect.centerx = int(x)
        self.__rect.centery = int(y)
        super(Explosion, self).setPos(x, y)

    def update(self):
        if self.state == Explosion.ALIVE:
            if pygame.time.get_ticks() - self.__animTimer > \
               self.__explosionFrameDelay:
                self.setFrame(self.__curFrameIndex)
                self.__curFrameIndex += 1
                if self.__curFrameIndex == len(Explosion.imgs[self.__objType]):
                    self.state = Explosion.WASTED
                self.__animTimer = pygame.time.get_ticks()

    def render(self, surf):
        if self.state == Explosion.ALIVE:
            surf.blit(self.__img, (self.__rect.x, self.__rect.y))

    def isExpired(self):
        return self.state == Explosion.WASTED

    def getRect(self):
        return self.__rect
