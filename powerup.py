import pygame
import random
import audio
from spritesheet import SpriteSheet
from shipobj import ShipObj


POWERUP_APPEAR_DURATION_MS = 8000  # 8 seconds
POWERUP_TYPE_NUM = 1

powerUpFrames = [
                [
                    (0, 0, 30, 30),
                    (31, 0, 30, 30),
                    (62, 0, 30, 30),
                    (93, 0, 30, 30)
                ],
                [
                ]
            ]

"""
PowerUp Class
-------------
Floating power up (increase HP).
"""


class PowerUp(ShipObj):
    movStep = 0.5

    POWERUP01_TYPE = 0

    spriteSheet = [None] * POWERUP_TYPE_NUM
    imgs = [[] for n in range(POWERUP_TYPE_NUM)]

    def __init__(self, x, y, scrW, scrH, objType):
        super(PowerUp, self).__init__(None, False, -1)
        self.__objType = objType
        self.__rect = None
        self.x = x
        self.y = y
        self.__scrW = scrW
        self.__scrH = scrH
        for i in range(POWERUP_TYPE_NUM):
            if not PowerUp.spriteSheet[i]:
                PowerUp.spriteSheet[i] = SpriteSheet(
                                                "res/img/powerup%02d.png" %
                                                (i + 1))
        if not PowerUp.imgs[objType]:
            for frames in powerUpFrames[objType]:
                PowerUp.imgs[objType].append(PowerUp.spriteSheet[objType].
                                             getFrame(*frames))
        self.__powerUpTimer = pygame.time.get_ticks()
        self.__animTimer = pygame.time.get_ticks()
        self.reset()
        self.setRandomDestRange(scrW // 5, 45 + self.getRect().height,
                                scrW - self.getRect().width,
                                scrH - self.getRect().height)
        self.generateRandomDest()
        self.__randStep = PowerUp.movStep + random.randint(0, 200) / 1000

    def reset(self):
        self.__curFrameIndex = 0
        self.state = PowerUp.ALIVE
        self.setFrame(0)

    def setFrame(self, frameIndex):
        self.__img = (PowerUp.imgs[self.__objType])[frameIndex]
        self.__rect = self.__img.get_rect()
        self.setPos(self.x, self.y)

    def setPos(self, x, y):
        self.__rect.centerx = int(x)
        self.__rect.centery = int(y)
        super(PowerUp, self).setPos(x, y)

    def update(self):
        if self.state == PowerUp.ALIVE:
            if self.isDestReached():
                self.generateRandomDest()
                # If power up expires just move away from screen
                if pygame.time.get_ticks() - self.__powerUpTimer > \
                   POWERUP_APPEAR_DURATION_MS:
                    if random.randint(0, 1):
                        self.destY = -self.getRect().height
                    else:
                        self.destY = self.__scrW + self.getRect().height
                    self.calcMoveSteps()
                self.__randStep = PowerUp.movStep + random.randint(0, 200) / \
                    1000
            else:
                self.moveToDest(self.__randStep)
                self.setPos(self.x, self.y)

            self.animate()

            if self.__rect.right <= 0 or \
               self.__rect.top >= self.__scrH or \
               self.__rect.bottom <= 0:
                self.state = PowerUp.WASTED

    def animate(self):
        if pygame.time.get_ticks() - self.__animTimer > 40:
            self.setFrame(self.__curFrameIndex)
            self.__curFrameIndex += 1
            if self.__curFrameIndex == len(PowerUp.imgs[self.__objType]):
                self.__curFrameIndex = 0
            self.__animTimer = pygame.time.get_ticks()

    def render(self, surf):
        if self.state == PowerUp.ALIVE:
            surf.blit(self.__img, (self.__rect.x, self.__rect.y))

    def isExpired(self):
        return self.state == PowerUp.WASTED

    def getRect(self):
        return self.__rect

    def doPowerUp(self, obj):
        if self.__objType == self.POWERUP01_TYPE:
            audio.playSoundEffect('hppowerup.wav')
            obj.updateHP(20)

    def isCollide(self, obj):
        if self.state != PowerUp.ALIVE or obj.state != ShipObj.ALIVE:
            return False
        if self.getRect().colliderect(obj.getRect()):
            self.doPowerUp(obj)
            self.state = PowerUp.WASTED
            return True
        return False

    def setExplosion(self):
        pass

    def getReward(self):
        pass

    def shoot(self):
        pass
