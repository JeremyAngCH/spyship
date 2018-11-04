from abc import ABC, abstractmethod
from gameobj import GameObj

"""
GameHitObj Class
----------------
Define behaviours for destructible game object.
"""


class GameHitObj(GameObj):

    def __init__(self, x, y, isHitable):
        super(GameHitObj, self).__init__(x, y)
        self.isHitable = isHitable

    def getDamage(self):
        return 0

    @abstractmethod
    def isCollide(self, obj):
        pass

    @abstractmethod
    def setExplosion(self):
        pass
