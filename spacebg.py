import pygame
import random
from gameobj import GameObj

SPACEBG_SCROLL_SPEED = 0.08

"""
SpaceBG Class
-------------
Scrolling space background.
"""


class SpaceBG(GameObj):
    NORMAL = 0
    FLIPX = 1
    FLIPY = 2

    def __init__(self, scrW, scrH, xSpeed=SPACEBG_SCROLL_SPEED):
        super(SpaceBG, self).__init__(0, 0)
        self.dx = xSpeed
        self.__spaceImg = pygame.image.load('res/img/spacebg.png').convert()
        self.__imgPattern = [
                                self.__spaceImg,
                                pygame.transform.flip(self.__spaceImg,
                                                      True, False),
                                pygame.transform.flip(self.__spaceImg,
                                                      False, True)
                            ]

        mapW = (scrW // self.__spaceImg.get_width()) + 1
        mapH = (scrH // self.__spaceImg.get_height())
        self.__spaceImgMap = [[0 for x in range(mapW)] for y in range(mapH)]
        for y in range(mapH):
            curMap = self.__spaceImgMap[y]
            for x in range(mapW):
                curMap[x] = random.randint(SpaceBG.NORMAL, SpaceBG.FLIPY)

    # Create endless scrolling illusion.
    def __shiftImgMap(self):
        for y in range(len(self.__spaceImgMap)):
            curMap = self.__spaceImgMap[y]
            for x in range(len(curMap)):
                if x == (len(curMap) - 1):
                    curMap[x] = random.randint(SpaceBG.NORMAL, SpaceBG.FLIPY)
                else:
                    curMap[x] = curMap[x + 1]

    def update(self):
        pass

    def render(self, surf):
        posY = 0
        for y in range(len(self.__spaceImgMap)):
            posX = 0
            curMap = self.__spaceImgMap[y]
            for x in range(len(curMap)):
                surf.blit(self.__imgPattern[curMap[x]],
                          (posX - int(self.x), posY))
                posX += self.__spaceImg.get_width()
            posY += self.__spaceImg.get_height()
        self.x += self.dx
        if self.x > self.__spaceImg.get_width():
            self.x -= self.__spaceImg.get_width()
            self.__shiftImgMap()

    def isExpired(self):
        return False

    def getRect(self):
        return None
