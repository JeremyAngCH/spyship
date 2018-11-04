from abc import ABC, abstractmethod

"""
BaseObj Class
-------------
Base for game object.
"""


class BaseObj(ABC):
    # Basic states for game object
    ALIVE = 0
    WASTED = 2
    UNUSED = 3

    def __init__(self, x=0.0, y=0.0, visible=True):
        self.x = x
        self.y = y
        self.visible = visible

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def isExpired(self):
        return False

    def setUnused(self):
        self.state = BaseObj.UNUSED

    def isUnused(self):
        return self.state == BaseObj.UNUSED

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self, surf):
        pass

    @abstractmethod
    def getRect(self):
        return None
