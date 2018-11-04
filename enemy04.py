import pygame
import random
import audio
from spritesheet import SpriteSheet
from shipobj import ShipObj
from bullet import Bullet
from explosion import Explosion
from shipfire import ShipFire

shipFrames = [
                (1, 0, 69, 86),
                (72, 0, 69, 86),
                (143, 0, 69, 86),
                (213, 0, 70, 86)
            ]

"""
Enemy04 Class
-------------
Big green alien space ship with wide shooting angle.
"""


class Enemy04(ShipObj):
    movStep = 0.25

    shipSpriteSheet = None
    imgs = []

    def __init__(self, spawn, x, y, scrW, scrH, shipID, isHitable):
        super(Enemy04, self).__init__(spawn, isHitable, shipID)
        self.HP = 200
        self.__explosion = []
        for i in range(4):
            self.__explosion.append(Explosion(0, 0,
                                              Explosion.EXPLOSION01_TYPE))
        self.__fire = [ShipFire(0, 0, ShipFire.SHIPFIRE02_TYPE),
                       ShipFire(0, 0, ShipFire.SHIPFIRE02_TYPE)]
        self.state = Enemy04.ALIVE
        self.__lastBtnReleased = True
        self.__isShooting = False
        self.__scrW = scrW
        self.__scrH = scrH
        self.__shipRect = None
        self.__curFrameIndex = 0

        if not Enemy04.shipSpriteSheet:
            Enemy04.shipSpriteSheet = SpriteSheet("res/img/enemyship04.png")

        if not Enemy04.imgs:
            for frames in shipFrames:
                Enemy04.imgs.append(Enemy04.shipSpriteSheet.getFrame(*frames))
        self.setShipFrame(0)
        self.setPos(x, y)
        self.__shipAnimTimer = pygame.time.get_ticks()
        self.__shootingTimer = pygame.time.get_ticks()
        self.setupBulletPool(Bullet.BULLET02_TYPE, scrW, scrH, 20)
        self.setRandomDestRange(scrW // 1.75, self.getRect().height // 2,
                                scrW - self.getRect().width // 2, scrH -
                                self.getRect().height // 2)
        self.generateRandomDest()
        self.__randStep = Enemy04.movStep + random.randint(0, 100) / 1000

    def setShipFrame(self, frameIndex):
        self.__shipImg = Enemy04.imgs[frameIndex]
        self.__shipRect = self.__shipImg.get_rect()

    def setPos(self, x, y):
        self.__shipRect.centerx = int(x)
        self.__shipRect.centery = int(y)
        self.__fire[0].setPos(self.__shipRect.right +
                              (self.__fire[0].getRect().width // 2),
                              self.__shipRect.centery - 19)
        self.__fire[1].setPos(self.__shipRect.right +
                              (self.__fire[1].getRect().width // 2),
                              self.__shipRect.centery + 19)
        super(Enemy04, self).setPos(x, y)

    def update(self):
        if self.state != Enemy04.ALIVE:
            if self.state == Enemy04.EXPLODE:
                for i in range(4):
                    if not self.__explosion[i].isExpired():
                        self.__explosion[i].update()
                    else:
                        self.state = Enemy04.WASTED
            return

        self.animateShip()
        self.__fire[0].update()
        self.__fire[1].update()

        if self.isDestReached():
            self.generateRandomDest()
            self.__randStep = Enemy04.movStep + random.randint(0, 200) / 1000
        else:
            self.moveToDest(self.__randStep)
        self.setPos(self.x, self.y)

        self.shoot()

    def render(self, surf):
        if self.state == Enemy04.ALIVE:
            self.__fire[0].render(surf)
            self.__fire[1].render(surf)
            surf.blit(self.__shipImg, (self.__shipRect.x, self.__shipRect.y))
        elif self.state == Enemy04.EXPLODE:
            for i in range(4):
                self.__explosion[i].render(surf)

    def animateShip(self):
        if pygame.time.get_ticks() - self.__shipAnimTimer > 70:
            self.setShipFrame(self.__curFrameIndex)
            self.__curFrameIndex += 1
            self.__curFrameIndex %= len(Enemy04.imgs)
            self.__shipAnimTimer = pygame.time.get_ticks()

    def shoot(self):
        if pygame.time.get_ticks() - self.__shootingTimer > 300:
            if random.randint(0, 4) == 0:
                # Shoot 3 bullets at once.
                # 1 bullet moving straight.
                # Another 2 bullets moving in -45 and +45 degrees.
                bulletDy = [0.7071, 0, -0.7071]
                for i in range(3):
                    bullet = self.getBulletFromPool()
                    if bullet:
                        bullet.setMovement(-1.0, bulletDy[i], 1.2)
                        bullet.setPos(self.__shipRect.left -
                                      (bullet.getRect().width // 2),
                                      self.__shipRect.centery)
                        Enemy04.spawnMan.addEnemyBullet(bullet)
            self.__shootingTimer = pygame.time.get_ticks()

    def isExpired(self):
        return self.state == Enemy04.WASTED

    def getRect(self):
        return self.__shipRect

    def getDamage(self):
        return -40

    def setExplosion(self):
        self.state = Enemy04.EXPLODE
        w = self.getRect().width // 4
        h = self.getRect().height // 4
        self.__explosion[0].setPos(self.x - w - random.randint(0, 10),
                                   self.y - h - random.randint(0, 10))
        self.__explosion[1].setPos(self.x + w + random.randint(0, 10),
                                   self.y - h - random.randint(0, 10))
        self.__explosion[2].setPos(self.x - w - random.randint(0, 10),
                                   self.y + h + random.randint(0, 10))
        self.__explosion[3].setPos(self.x + w + random.randint(0, 10),
                                   self.y + h + random.randint(0, 10))
        audio.playSoundEffect('bexp.wav')

    def getReward(self):
        return 75
