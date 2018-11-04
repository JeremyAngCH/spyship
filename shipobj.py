import random
from abc import ABC, abstractmethod
from gamehitobj import GameHitObj
from bullet import Bullet

SCORE_MAX = 9999999

"""
ShipObj Class
-------------
Define basic behaviours for all spaceships.
"""


class ShipObj(GameHitObj):

    spawnMan = None

    def __init__(self, spawn, isHitable, shipID, godMode=False):
        super(ShipObj, self).__init__(0, 0, isHitable)
        if not ShipObj.spawnMan:
            ShipObj.spawnMan = spawn
        self.shipID = shipID
        self.godMode = godMode
        self.HP = 0
        self.score = 0
        self.__bulletPool = []
        self.__randMinX = self.__randMinY = self.__randMaxX = \
            self.__randMaxY = 0

    def setUnused(self):
        super(ShipObj, self).setUnused()
        if self.shipID >= 0:
            ShipObj.spawnMan.updateObjsCount(self.shipID, -1)

    def setGodMode(self, godMode):
        self.godMode = godMode

    def updateHP(self, p):
        self.HP += p
        if self.HP <= 0:
            self.setExplosion()

    def updateScore(self, s):
        if self.state == ShipObj.ALIVE:
            self.score += s
            if self.score > SCORE_MAX:
                self.score = SCORE_MAX

    # Pre-allocate bullets and reuse them from the pools.
    def setupBulletPool(self, bulletType, scrW, scrH, num):
        for i in range(num):
            bullet = Bullet(self, 0, 0, scrW, scrH, bulletType, 1, 0)
            bullet.setUnused()
            self.__bulletPool.append(bullet)

    def getBulletFromPool(self):
        for i in range(len(self.__bulletPool)):
            if self.__bulletPool[i].isUnused():
                self.__bulletPool[i].reset()
                return self.__bulletPool[i]
        return None

    # Set the moving area (used by enemy spaceships)
    def setRandomDestRange(self, minX, minY, maxX, maxY):
        self.__randMinX, self.__randMinY, self.__randMaxX, self.__randMaxY = \
            (minX, minY, maxX, maxY)

    # Pick a random location to travel to (used by enemy spaceships)
    def generateRandomDest(self):
        self.destX = random.randint(self.__randMinX, self.__randMaxX)
        self.destY = random.randint(self.__randMinY, self.__randMaxY)
        self.calcMoveSteps()

    # Check whether spaceship collides with other spaceships or bullets.
    def isCollide(self, obj):
        if not self.isHitable or self.state != ShipObj.ALIVE or \
           obj.state != ShipObj.ALIVE:
            return False
        if self.getRect().colliderect(obj.getRect()):
            self.updateHP(obj.getDamage())
            if isinstance(obj, ShipObj):
                obj.updateHP(self.getDamage())
            else:
                obj.setExplosion()
            if self.HP <= 0 and isinstance(obj, Bullet):
                obj.getOwner().updateScore(self.getReward())
            return True
        return False

    def shoot(self):
        pass

    @abstractmethod
    def getReward(self):
        pass
