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
                (0, 0, 88, 100),
                (89, 0, 88, 100),
                (178, 0, 88, 100),
                (267, 0, 88, 100)
            ]

shipCannonFrame = (356, 10, 80, 80)

"""
Enemy05 Class
-------------
Big red alien space ship with rotating cannon.
"""


class Enemy05(ShipObj):
    movStep = 0.25

    shipSpriteSheet = None
    imgs = []
    cannonImg = None

    def __init__(self, spawn, x, y, scrW, scrH, shipID, isHitable):
        super(Enemy05, self).__init__(spawn, isHitable, shipID)
        self.HP = 600
        self.__explosion = []
        for i in range(4):
            self.__explosion.append(Explosion(0, 0,
                                              Explosion.EXPLOSION01_TYPE))
        self.__fire = [ShipFire(0, 0, ShipFire.SHIPFIRE02_TYPE),
                       ShipFire(0, 0, ShipFire.SHIPFIRE02_TYPE),
                       ShipFire(0, 0, ShipFire.SHIPFIRE02_TYPE)]
        self.state = Enemy05.ALIVE
        self.__lastBtnReleased = True
        self.__isShooting = False
        self.__scrW = scrW
        self.__scrH = scrH
        self.__shipRect = None
        self.__curFrameIndex = 0

        if not Enemy05.shipSpriteSheet:
            Enemy05.shipSpriteSheet = SpriteSheet("res/img/enemyship05.png")

        if not Enemy05.imgs:
            for frames in shipFrames:
                Enemy05.imgs.append(Enemy05.shipSpriteSheet.getFrame(*frames))

        if not Enemy05.cannonImg:
            Enemy05.cannonImg = Enemy05.shipSpriteSheet.getFrame(
                                                            *shipCannonFrame)
        self.__cannonDegree = 0.0
        self.__cannonImg = pygame.transform.rotate(Enemy05.cannonImg,
                                                   self.__cannonDegree)
        self.__cannonRect = self.__cannonImg.get_rect()
        self.__cannonRadius = self.__cannonRect.width // 2
        self.__moveCannonCW = True
        self.__cannonMoveTimer = pygame.time.get_ticks()
        self.setShipFrame(0)
        self.setPos(x, y)
        self.__shipAnimTimer = pygame.time.get_ticks()
        self.__shootingTimer = pygame.time.get_ticks()
        self.setupBulletPool(Bullet.BULLET02_TYPE, scrW, scrH, 30)
        self.setRandomDestRange(scrW // 1.5, self.getRect().height // 2,
                                scrW - self.getRect().width // 2, scrH -
                                self.getRect().height // 2)
        self.generateRandomDest()
        self.__randStep = Enemy05.movStep + random.randint(0, 100) / 1000

    def setShipFrame(self, frameIndex):
        self.__shipImg = Enemy05.imgs[frameIndex]
        self.__shipRect = self.__shipImg.get_rect()

    def setPos(self, x, y):
        self.__shipRect.centerx = int(x)
        self.__shipRect.centery = int(y)
        self.__cannonRect.centerx = int(x + 6)
        self.__cannonRect.centery = int(y)
        self.__fire[0].setPos(self.__shipRect.right +
                              (self.__fire[0].getRect().width // 2),
                              self.__shipRect.centery - 25)
        self.__fire[1].setPos(self.__shipRect.right +
                              (self.__fire[1].getRect().width // 2),
                              self.__shipRect.centery)
        self.__fire[2].setPos(self.__shipRect.right +
                              (self.__fire[2].getRect().width // 2),
                              self.__shipRect.centery + 25)
        super(Enemy05, self).setPos(x, y)

    def update(self):
        if self.state != Enemy05.ALIVE:
            if self.state == Enemy05.EXPLODE:
                for i in range(4):
                    if not self.__explosion[i].isExpired():
                        self.__explosion[i].update()
                    else:
                        self.state = Enemy05.WASTED
            return

        self.animateShip()
        for i in range(3):
            self.__fire[i].update()

        if self.isDestReached():
            self.generateRandomDest()
            self.__randStep = Enemy05.movStep + random.randint(0, 200) / 1000
        else:
            self.moveToDest(self.__randStep)
        self.setPos(self.x, self.y)

        self.shoot()

    def render(self, surf):
        if self.state == Enemy05.ALIVE:
            for i in range(3):
                self.__fire[i].render(surf)
            surf.blit(self.__shipImg, (self.__shipRect.x, self.__shipRect.y))
            surf.blit(self.__cannonImg, (self.__cannonRect.x,
                                         self.__cannonRect.y))
        elif self.state == Enemy05.EXPLODE:
            for i in range(4):
                self.__explosion[i].render(surf)

    def rotateCannon(self):
        # Cannon rotate between 45 and -45 degrees
        if self.__moveCannonCW:
            self.__cannonDegree += 3
            if self.__cannonDegree >= 45:
                self.__cannonDegree = 45
                self.__moveCannonCW = False
        else:
            self.__cannonDegree -= 3
            if self.__cannonDegree <= -45:
                self.__cannonDegree = -45
                self.__moveCannonCW = True
        self.__cannonImg = pygame.transform.rotate(Enemy05.cannonImg,
                                                   self.__cannonDegree)
        self.__cannonRect = self.__cannonImg.get_rect()
        self.__cannonRect.centerx = int(self.x)
        self.__cannonRect.centery = int(self.y)

    def animateShip(self):
        if pygame.time.get_ticks() - self.__cannonMoveTimer > 30:
            self.rotateCannon()
            self.__cannonMoveTimer = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.__shipAnimTimer > 70:
            self.setShipFrame(self.__curFrameIndex)
            self.__curFrameIndex += 1
            self.__curFrameIndex %= len(Enemy05.imgs)
            self.__shipAnimTimer = pygame.time.get_ticks()

    def shoot(self):
        if pygame.time.get_ticks() - self.__shootingTimer > 250:
            bullet = self.getBulletFromPool()
            if bullet:
                # Bullet move according to the cannon's angle
                dx = sincoslookup.cosLookupTbl[
                    abs(int(self.__cannonDegree))]
                dy = sincoslookup.sinLookupTbl[
                    abs(int(self.__cannonDegree))]
                if self.__cannonDegree < 0:
                    dy = -dy
                bullet.setMovement(-dx, dy, 0.9)
                # Place the bullet at the cannon's muzzle
                r = self.__cannonRadius + bullet.getRect().width // 2
                bullet.setPos(self.__cannonRect.centerx - r * dx,
                              self.__cannonRect.centery + r * dy)
                Enemy05.spawnMan.addEnemyBullet(bullet)
            self.__shootingTimer = pygame.time.get_ticks()

    def isExpired(self):
        return self.state == Enemy05.WASTED

    def getRect(self):
        return self.__shipRect

    def getDamage(self):
        return -1000

    def setExplosion(self):
        self.state = Enemy05.EXPLODE
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
        return 150
