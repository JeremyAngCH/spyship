import pygame
import random
import audio
import sincoslookup
from spritesheet import SpriteSheet
from shipobj import ShipObj
from bullet import Bullet
from explosion import Explosion
from shipfire import ShipFire

shipFrames = [
                (0, 0, 40, 26),
                (41, 2, 40, 19),
                (82, 5, 40, 16),
                (123, 5, 40, 19)
            ]

FLYING_SINE_AMPLITUDE = 78

"""
Enemy03 Class
-------------
Fast flying rotating space rocket.
"""


class Enemy03(ShipObj):
    movStep = 1.5

    shipSpriteSheet = None
    imgs = []

    def __init__(self, spawn, x, y, scrW, scrH, shipID, isHitable, shiftPhase):
        super(Enemy03, self).__init__(spawn, isHitable, shipID)
        self.HP = 5
        self.__explosion = Explosion(0, 0, Explosion.EXPLOSION01_TYPE)
        self.__fire = ShipFire(0, 0, ShipFire.SHIPFIRE02_TYPE)
        self.state = Enemy03.ALIVE
        self.__lastBtnReleased = True
        self.__isShooting = False
        self.__scrW = scrW
        self.__scrH = scrH
        self.__shipRect = None
        self.__curFrameIndex = 0
        self.__originY = y
        # Shift the phase or offset of the sine wave so that 2 rockets can
        # travel in opposite direction
        self.__degree = 180 if shiftPhase else 0
        if not Enemy03.shipSpriteSheet:
            Enemy03.shipSpriteSheet = SpriteSheet("res/img/enemyship03.png")

        if not Enemy03.imgs:
            for frames in shipFrames:
                Enemy03.imgs.append(Enemy03.shipSpriteSheet.getFrame(*frames))
        self.setShipFrame(0)
        self.setPos(x, y)
        self.__shipAnimTimer = pygame.time.get_ticks()
        self.setupBulletPool(Bullet.BULLET02_TYPE, scrW, scrH, 10)

    def setShipFrame(self, frameIndex):
        self.__shipImg = Enemy03.imgs[frameIndex]
        self.__shipRect = self.__shipImg.get_rect()

    def setPos(self, x, y):
        self.__shipRect.centerx = int(x)
        self.__shipRect.centery = int(y)
        self.__fire.setPos(self.__shipRect.right +
                           (self.__fire.getRect().width // 2),
                           self.__shipRect.centery)
        super(Enemy03, self).setPos(x, y)

    def update(self):
        if self.state != Enemy03.ALIVE:
            if self.state == Enemy03.EXPLODE:
                if not self.__explosion.isExpired():
                    self.__explosion.update()
                else:
                    self.state = Enemy03.WASTED
            return

        self.animateShip()
        self.__fire.update()

        # Sine wave flying motion
        self.setPos(self.x - Enemy03.movStep, self.__originY +
                    (sincoslookup.sinLookupTbl[self.__degree] *
                     FLYING_SINE_AMPLITUDE))
        self.__degree += 1
        if self.__degree >= 360:
            self.__degree = 0

        # Remove itself from the game scene if it flies beyond the left
        # edge of the screen.
        if self.__shipRect.right <= 0:
            self.state = Enemy03.WASTED

    def render(self, surf):
        if self.state == Enemy03.ALIVE:
            self.__fire.render(surf)
            surf.blit(self.__shipImg, (self.__shipRect.x, self.__shipRect.y))
        elif self.state == Enemy03.EXPLODE:
            self.__explosion.render(surf)

    def animateShip(self):
        if pygame.time.get_ticks() - self.__shipAnimTimer > 70:
            self.setShipFrame(self.__curFrameIndex)
            self.__curFrameIndex += 1
            self.__curFrameIndex %= len(Enemy03.imgs)
            self.__shipAnimTimer = pygame.time.get_ticks()

    def isExpired(self):
        return self.state == Enemy03.WASTED

    def getRect(self):
        return self.__shipRect

    def getDamage(self):
        return -20

    def setExplosion(self):
        self.state = Enemy03.EXPLODE
        self.__explosion.setPos(self.x, self.y)
        audio.playSoundEffect('eexp.wav')

    def getReward(self):
        return 25
