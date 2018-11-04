import pygame
import random
from spritesheet import SpriteSheet
from gameobj import GameObj

# 2 types of bitmap font (Small & Big)
BMP_FONT_TYPE_NUM = 2
# 16 characters per row
BMP_FONT_COL_NUM = 16
# 4 rows of 16 characters
BMP_FONT_ROW_NUM = 4
# Character map start from minimum ASCII number 32 which is 'SPACE'
BMP_FONT_CHAR_MIN = 32
# Maximum ASCII number in the character map is 32 + (4 * 16) - 1 = 95
BMP_FONT_CHAR_MAX = 32 + (BMP_FONT_ROW_NUM * BMP_FONT_COL_NUM) - 1

# Dimension information for extracting character from character map
# [width, height, gap]
bmpFontInfo = [[17, 21, 1], [20, 26, 2]]

"""
BmpText Class
-------------
Bitmap text renderer.
"""


class BmpText(GameObj):
    # Font sizes
    SMALL_FNT = 0
    BIG_FNT = 1

    # Font alignments
    LEFT_ALIGN = 0
    CENTER_ALIGN = 1
    RIGHT_ALIGN = 2

    spriteSheet = [None] * BMP_FONT_TYPE_NUM
    imgs = [[] for n in range(BMP_FONT_TYPE_NUM)]

    def __init__(self, x, y, text="", fntType=SMALL_FNT, align=CENTER_ALIGN,
                 visible=True, blink=False):
        super(BmpText, self).__init__(x, y, 0, 0, visible)
        self.state = BmpText.ALIVE
        for i in range(BMP_FONT_TYPE_NUM):
            if not BmpText.spriteSheet[i]:
                # Load characters map
                BmpText.spriteSheet[i] = SpriteSheet(
                                                "res/img/character%02d.png" %
                                                (i + 1))
        if not BmpText.imgs[0]:
            for i in range(BMP_FONT_TYPE_NUM):
                for fntRow in range(BMP_FONT_ROW_NUM):
                    for fntCol in range(BMP_FONT_COL_NUM):
                        # Load all individual character to each bitmap surface
                        BmpText.imgs[i].append(
                            BmpText.spriteSheet[i].getFrame(
                                fntCol * ((bmpFontInfo[i])[0] + 1),
                                fntRow * ((bmpFontInfo[i])[1] + 1),
                                (bmpFontInfo[i])[0],
                                (bmpFontInfo[i])[1]))
        self.__fntType = fntType
        self.__align = align
        self.setText(text)
        self.setBlink(blink)

    def setBlink(self, blink):
        self.__blink = blink
        self.__blinkTimer = pygame.time.get_ticks()
        self.visible = True

    def updateTextSize(self):
        self.__textWidth = self.__textLen * ((bmpFontInfo[self.__fntType])[0] +
                                             (bmpFontInfo[self.__fntType])[2])
        self.__textHeight = (bmpFontInfo[self.__fntType])[1]

    def updateTextPos(self):
        self.__textStartX = self.x
        if self.__align == BmpText.CENTER_ALIGN:
            self.__textStartX -= (self.__textWidth // 2)
        elif self.__align == BmpText.RIGHT_ALIGN:
            self.__textStartX -= self.__textWidth

    def getText(self):
        return self.__text

    def setText(self, text):
        self.__text = text.upper()
        self.__textLen = len(text)
        self.updateTextSize()
        self.updateTextPos()

    def setFntType(self, fntType):
        self.__fntType = fntType
        self.updateTextSize()
        self.updateTextPos()

    def setAlignment(self, align):
        self.__align = align
        self.updateTextPos()

    def setPos(self, x, y):
        super(Explosion, self).setPos(x, y)
        self.updateTextPos()

    def update(self):
        if self.__blink:
            if pygame.time.get_ticks() - self.__blinkTimer > 150:
                # Toggle visiblity if blinking
                self.visible = not self.visible
                self.__blinkTimer = pygame.time.get_ticks()

    def render(self, surf):
            if not self.__textLen:
                return
            startX = self.__textStartX
            fntWidth = (bmpFontInfo[self.__fntType])[0] + \
                       (bmpFontInfo[self.__fntType])[2]
            for c in self.__text:
                # Convert a character in the string to ASCII number
                asc = ord(c)
                if asc >= BMP_FONT_CHAR_MIN and asc <= BMP_FONT_CHAR_MAX:
                    # Convert the ASCII number to ordinal which is used
                    # to represent the position of bitmap character.
                    # ASCII number 32 = 0 (1st bitmap character)
                    # ASCII number 33 = 1 (2nd bitmap character)
                    # and so on...
                    asc -= BMP_FONT_CHAR_MIN
                    surf.blit((BmpText.imgs[self.__fntType])[asc], (startX,
                              self.y - (self.__textHeight // 2)))
                    startX += fntWidth

    def getRect(self):
        return None
