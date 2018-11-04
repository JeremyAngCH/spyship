from baseobj import BaseObj

"""
GameObj Class
-------------
Define basic behaviours for all movable game object.
"""


class GameObj(BaseObj):

    EXPLODE = BaseObj.UNUSED + 1

    def __init__(self, x=0.0, y=0.0, dx=0.0, dy=0.0, visible=True):
        super(GameObj, self).__init__(x, y, visible)
        self.dx = dx
        self.dy = dy
        self.destX = 0
        self.destY = 0
        self.state = GameObj.UNUSED

    def setDest(self, x, y):
        self.destX = x
        self.destY = y

    def calcMoveSteps(self):
        dx = self.destX - int(self.x)
        dy = self.destY - int(self.y)
        dydx = (dy / abs(dx)) if dx != 0 else dy
        dxdy = (dx / abs(dy)) if dy != 0 else dx
        self.dy = (dydx / abs(dydx)) if abs(dydx) > 1 else dydx
        self.dx = (dxdy / abs(dxdy)) if abs(dxdy) > 1 else dxdy

    def moveToDest(self, speed):
        self.x += float(self.dx * speed)
        self.y += float(self.dy * speed)
        if (self.dx < 0 and self.x < self.destX) or \
           (self.dx > 0 and self.x > self.destX):
            self.x = float(self.destX)
        if (self.dy < 0 and self.y < self.destY) or \
           (self.dy > 0 and self.y > self.destY):
            self.y = float(self.destY)

    def isDestReached(self):
        return self.x == self.destX and self.y == self.destY
