import pygame
import random
import audio
from spritesheet import SpriteSheet
from shipobj import ShipObj
from bullet import Bullet
from explosion import Explosion
from shipfire import ShipFire

shipFrames = [
                (1, 0, 39, 42),
                (43, 1, 38, 40),
                (85, 2, 37, 38),
                (123, 1, 40, 40)
            ]

"""
Enemy02 Class
-------------
Small and slower flying alien space ship with shooting capability.
"""


class Enemy02(ShipObj):
    movStep = 0.4

    shipSpriteSheet = None
    imgs = []

    def __init__(self, spawn, x, y, scrW, scrH, shipID, isHitable):
        super(Enemy02, self).__init__(spawn, isHitable, shipID)
        self.HP = 20
        self.__explosion = Explosion(0, 0, Explosion.EXPLOSION01_TYPE)
        self.__fire = ShipFire(0, 0, ShipFire.SHIPFIRE02_TYPE)
        self.state = Enemy02.ALIVE
        self.__lastBtnReleased = True
        self.__isShooting = False
        self.__scrW = scrW
        self.__scrH = scrH
        self.__shipRect = None
        self.__curFrameIndex = 0

        if not Enemy02.shipSpriteSheet:
            Enemy02.shipSpriteSheet = SpriteSheet("res/img/enemyship02.png")

        if not Enemy02.imgs:
            for frames in shipFrames:
                Enemy02.imgs.append(Enemy02.shipSpriteSheet.getFrame(*frames))
        self.setShipFrame(0)
        self.setPos(x, y)
        self.__shipAnimTimer = pygame.time.get_ticks()
        self.__shootingTimer = pygame.time.get_ticks()
        self.setupBulletPool(Bullet.BULLET02_TYPE, scrW, scrH, 10)
        # Set the moving area of the spaceship
        self.setRandomDestRange(scrW // 2, 45, scrW - self.getRect().width,
                                scrH - 5)
        # Select a random spot within the moving area as the flying destination
        self.generateRandomDest()
        self.__randStep = Enemy02.movStep + random.randint(0, 200) / 1000

    def setShipFrame(self, frameIndex):
        self.__shipImg = Enemy02.imgs[frameIndex]
        self.__shipRect = self.__shipImg.get_rect()

    def setPos(self, x, y):
        self.__shipRect.centerx = int(x)
        self.__shipRect.centery = int(y)
        self.__fire.setPos(self.__shipRect.right +
                           (self.__fire.getRect().width // 2),
                           self.__shipRect.centery)
        super(Enemy02, self).setPos(x, y)

    def update(self):
        if self.state != Enemy02.ALIVE:
            if self.state == Enemy02.EXPLODE:
                if not self.__explosion.isExpired():
                    self.__explosion.update()
                else:
                    self.state = Enemy02.WASTED
            return

        self.animateShip()
        self.__fire.update()

        if self.isDestReached():
            self.generateRandomDest()
            # Fly with different speed
            self.__randStep = Enemy02.movStep + random.randint(0, 200) / 1000
        else:
            self.moveToDest(self.__randStep)
        self.setPos(self.x, self.y)

        self.shoot()

    def render(self, surf):
        if self.state == Enemy02.ALIVE:
            self.__fire.render(surf)
            surf.blit(self.__shipImg, (self.__shipRect.x, self.__shipRect.y))
        elif self.state == Enemy02.EXPLODE:
            self.__explosion.render(surf)

    def animateShip(self):
        if pygame.time.get_ticks() - self.__shipAnimTimer > 70:
            self.setShipFrame(self.__curFrameIndex)
            self.__curFrameIndex += 1
            self.__curFrameIndex %= len(Enemy02.imgs)
            self.__shipAnimTimer = pygame.time.get_ticks()

    def shoot(self):
        if pygame.time.get_ticks() - self.__shootingTimer > 300:
            if random.randint(0, 5) == 0:
                bullet = self.getBulletFromPool()
                if bullet:
                    bullet.setMovement(-1.0, 0, 1.5)
                    bullet.setPos(self.__shipRect.left -
                                  (bullet.getRect().width // 2),
                                  self.__shipRect.centery)
                    Enemy02.spawnMan.addEnemyBullet(bullet)
            self.__shootingTimer = pygame.time.get_ticks()

    def isExpired(self):
        return self.state == Enemy02.WASTED

    def getRect(self):
        return self.__shipRect

    def getDamage(self):
        return -20

    def setExplosion(self):
        self.state = Enemy02.EXPLODE
        self.__explosion.setPos(self.x, self.y)
        audio.playSoundEffect('eexp.wav')

    def getReward(self):
        return 20
