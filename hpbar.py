import pygame
import random
from spritesheet import SpriteSheet
from gameobj import GameObj

# 100% HP = 5 bars
HP_BAR_MAX = 5

"""
HPBar Class
-----------
Player's Health points
"""


class HPBar(GameObj):

    spriteSheet = None

    def __init__(self, x, y, hp):
        super(HPBar, self).__init__()
        self.setBar(hp)
        self.x = x
        self.y = y
        if not HPBar.spriteSheet:
            HPBar.spriteSheet = SpriteSheet("res/img/hpbar.png")
        self.__hpframe = HPBar.spriteSheet.getFrame(0, 0, 78, 36)
        self.__rect = self.__hpframe.get_rect()
        self.__bar = HPBar.spriteSheet.getFrame(79, 9, 10, 18)
        self.__barRect = self.__bar.get_rect()
        self.__animTimer = pygame.time.get_ticks()
        self.reset()

    def setBar(self, hp):
        if hp < 0:
            hp = 0
        self.HPBarNum = int(hp * HP_BAR_MAX)
        if self.HPBarNum == 0 and hp > 0:
            self.HPBarNum = 1

    def reset(self):
        self.state = HPBar.ALIVE
        self.setPos(self.x, self.y)

    def setPos(self, x, y):
        self.__rect.x = int(x)
        self.__rect.y = int(y)
        super(HPBar, self).setPos(x, y)

    def update(self):
        pass

    def render(self, surf):
            if self.HPBarNum == 0:
                return
            surf.blit(self.__hpframe, (self.__rect.x, self.__rect.y))
            startX = 10
            for n in range(self.HPBarNum):
                surf.blit(self.__bar, (self.__rect.x + startX,
                                       self.__rect.y + 9))
                startX += (self.__barRect.width + 2)

    def getRect(self):
        return self.__rect
