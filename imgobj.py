import pygame
from baseobj import BaseObj

"""
ImgObj Class
------------
Simple class for rendering image on screen
"""


class ImgObj(BaseObj):

    NORMAL_STYLE = 0
    TOP_STYLE = 1
    CENTER_STYLE = 2

    def __init__(self, x, y, filename, style=NORMAL_STYLE):
        super(ImgObj, self).__init__(x, y)
        self.__img = pygame.image.load(filename).convert_alpha()
        self.__rect = self.__img.get_rect()
        self.__isAnimating = False
        self.__style = style
        self.__targetRect = self.__rect.copy()
        self.__animTimer = pygame.time.get_ticks()
        self.setPos(x, y)
        if style != ImgObj.NORMAL_STYLE:
            self.__isAnimating = True
        if style == ImgObj.TOP_STYLE:
            self.__targetRect.height = 0
        elif style == ImgObj.CENTER_STYLE:
            self.__targetRect.y = self.__targetRect.height // 2
            self.__targetRect.height = 0

    def isAnimating(self):
        return self.__isAnimating

    def setPos(self, x, y):
        self.__rect.centerx = int(x)
        self.__rect.centery = int(y)
        super(ImgObj, self).setPos(x, y)

    def update(self):
        if self.__isAnimating:
            if pygame.time.get_ticks() - self.__animTimer >= 25:
                if self.__targetRect.height < self.__rect.height:
                    if self.__style == ImgObj.TOP_STYLE:
                        self.__targetRect.height += 8
                    elif self.__style == ImgObj.CENTER_STYLE:
                        self.__targetRect.height += 2
                        self.__targetRect.y -= 1
                if self.__targetRect.height >= self.__rect.height:
                    self.__targetRect.y = 0
                    self.__targetRect.height = self.__rect.height
                    self.__isAnimating = False
                self.__animTimer = pygame.time.get_ticks()

    def render(self, surf):
        if not self.__isAnimating:
            surf.blit(self.__img, (self.__rect.x, self.__rect.y))
        else:
            surf.blit(self.__img, (self.__rect.x, self.__rect.y +
                                   self.__targetRect.y), self.__targetRect)

    def getRect(self):
        return self.__rect
