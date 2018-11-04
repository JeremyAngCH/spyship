import pygame
import random
import audio
from spritesheet import SpriteSheet
from shipobj import ShipObj
from bullet import Bullet
from explosion import Explosion
from shipfire import ShipFire

shipFrames = [
                (0, 0, 38, 44),
                (39, 0, 38, 44),
                (78, 0, 38, 44),
                (117, 0, 38, 44)
            ]

"""
Enemy01 Class
-------------
Small and fast flying alien space ship with no shooting capability.
"""


class Enemy01(ShipObj):
    movStep = 1.0

    shipSpriteSheet = None
    imgs = []

    def __init__(self, spawn, x, y, scrW, scrH, shipID, isHitable):
        super(Enemy01, self).__init__(spawn, isHitable, shipID)
        self.HP = 10
        self.__explosion = Explosion(0, 0, Explosion.EXPLOSION01_TYPE)
        self.__fire = ShipFire(0, 0, ShipFire.SHIPFIRE02_TYPE)
        self.state = Enemy01.ALIVE
        self.__lastBtnReleased = True
        self.__isShooting = False
        self.__scrW = scrW
        self.__scrH = scrH
        self.__shipRect = None
        self.__curFrameIndex = 0

        if not Enemy01.shipSpriteSheet:
            Enemy01.shipSpriteSheet = SpriteSheet("res/img/enemyship01.png")

        if not Enemy01.imgs:
            for frames in shipFrames:
                Enemy01.imgs.append(Enemy01.shipSpriteSheet.getFrame(*frames))
        self.setShipFrame(0)
        self.setPos(x, y)
        self.__shipAnimTimer = pygame.time.get_ticks()
        self.setupBulletPool(Bullet.BULLET02_TYPE, scrW, scrH, 10)
        self.setRandomDestRange(scrW // 3, 45, scrW - self.getRect().width,
                                scrH - 5)
        self.generateRandomDest()
        # Make sure the space ship always fly towards the
        # left edge of the screen.
        self.destX = -((self.getRect().width // 2) + 5)
        self.calcMoveSteps()
        self.__randStep = Enemy01.movStep + random.randint(0, 200) / 1000

    def setShipFrame(self, frameIndex):
        self.__shipImg = Enemy01.imgs[frameIndex]
        self.__shipRect = self.__shipImg.get_rect()

    def setPos(self, x, y):
        self.__shipRect.centerx = int(x)
        self.__shipRect.centery = int(y)
        self.__fire.setPos(self.__shipRect.right +
                           (self.__fire.getRect().width // 2),
                           self.__shipRect.centery)
        super(Enemy01, self).setPos(x, y)

    def update(self):
        if self.state != Enemy01.ALIVE:
            if self.state == Enemy01.EXPLODE:
                if not self.__explosion.isExpired():
                    self.__explosion.update()
                else:
                    self.state = Enemy01.WASTED
            return

        self.animateShip()
        self.__fire.update()

        if not self.isDestReached():
            self.moveToDest(self.__randStep)
        self.setPos(self.x, self.y)

        # Remove itself from the game scene if it flies beyond the left
        # edge of the screen.
        if self.__shipRect.right <= 0 or \
           self.__shipRect.top >= self.__scrH or \
           self.__shipRect.bottom <= 0:
            self.state = Enemy01.WASTED

    def render(self, surf):
        if self.state == Enemy01.ALIVE:
            self.__fire.render(surf)
            surf.blit(self.__shipImg, (self.__shipRect.x, self.__shipRect.y))
        elif self.state == Enemy01.EXPLODE:
            self.__explosion.render(surf)

    def animateShip(self):
        if pygame.time.get_ticks() - self.__shipAnimTimer > 70:
            self.setShipFrame(self.__curFrameIndex)
            self.__curFrameIndex += 1
            self.__curFrameIndex %= len(Enemy01.imgs)
            self.__shipAnimTimer = pygame.time.get_ticks()

    def isExpired(self):
        return self.state == Enemy01.WASTED

    def getRect(self):
        return self.__shipRect

    def getDamage(self):
        return -20

    def setExplosion(self):
        self.state = Enemy01.EXPLODE
        self.__explosion.setPos(self.x, self.y)
        audio.playSoundEffect('eexp.wav')

    def getReward(self):
        return 10
