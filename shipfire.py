import pygame
from spritesheet import SpriteSheet
from gameobj import GameObj

FIRE_TYPE_NUM = 2
fireFrames = [
                [
                    (0, 0, 13, 9),
                    (14, 0, 13, 9),
                    (28, 0, 13, 9),
                    (42, 0, 13, 9)
                ],
                [
                    (0, 0, 13, 10),
                    (14, 0, 13, 10),
                    (28, 0, 13, 10),
                    (42, 0, 13, 10)
                ]
            ]

"""
ShipFire Class
--------------
Spaceship fire animation.
"""


class ShipFire(GameObj):
    # Player's ship fire
    SHIPFIRE01_TYPE = 0
    # Enemy's ship fire
    SHIPFIRE02_TYPE = 1

    spriteSheet = [None] * FIRE_TYPE_NUM
    imgs = [[] for n in range(FIRE_TYPE_NUM)]

    def __init__(self, x, y, objType):
        super(ShipFire, self).__init__()
        self.__objType = objType
        self.__rect = None
        self.x = x
        self.y = y
        for i in range(FIRE_TYPE_NUM):
            if not ShipFire.spriteSheet[i]:
                ShipFire.spriteSheet[i] = SpriteSheet("res/img/fire%02d.png" %
                                                      (i + 1))
        if not ShipFire.imgs[objType]:
            for frames in fireFrames[objType]:
                ShipFire.imgs[objType].append(ShipFire.spriteSheet[objType].
                                              getFrame(*frames))
        self.__animTimer = pygame.time.get_ticks()
        self.reset()

    def reset(self):
        self.__curFrameIndex = 0
        self.state = ShipFire.ALIVE
        self.setFrame(0)

    def setFrame(self, frameIndex):
        self.__img = (ShipFire.imgs[self.__objType])[frameIndex]
        self.__rect = self.__img.get_rect()
        self.setPos(self.x, self.y)

    def setPos(self, x, y):
        self.__rect.centerx = int(x)
        self.__rect.centery = int(y)
        super(ShipFire, self).setPos(x, y)

    def update(self):
        if self.state == ShipFire.ALIVE:
            if pygame.time.get_ticks() - self.__animTimer > 25:
                self.setFrame(self.__curFrameIndex)
                self.__curFrameIndex += 1
                if self.__curFrameIndex == len(ShipFire.imgs[self.__objType]):
                    self.__curFrameIndex = 0
                self.__animTimer = pygame.time.get_ticks()

    def render(self, surf):
        if self.state == ShipFire.ALIVE:
            surf.blit(self.__img, (self.__rect.x, self.__rect.y))

    def isExpired(self):
        return self.state == ShipFire.WASTED

    def getRect(self):
        return self.__rect
