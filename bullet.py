import pygame
from spritesheet import SpriteSheet
from gameobj import GameObj

# 2 types of bullet
BULLET_TYPE_NUM = 2
# Dimension information for extracting animation frames from spritesheet
# [x, y, width, height]
bulletsFrames = [
                    [
                        (1, 4, 14, 7),
                        (17, 0, 16, 14),
                        (34, 0, 16, 14),
                        (51, 0, 16, 14),
                        (68, 0, 16, 14)
                    ],
                    [
                        (4, 4, 12, 12),
                        (21, 0, 20, 20),
                        (42, 0, 20, 20),
                        (63, 0, 20, 20)
                    ]
            ]

# Deduct 5 HP from enemy if hit by player's bullet
# Deduct 20 HP from player if hit by enemy's bullet
bulletsDamages = [-5, -20]

"""
Bullet Class
------------
Bullet game object.
"""


class Bullet(GameObj):
    # Player's bullet
    BULLET01_TYPE = 0
    # Enemy's bullet
    BULLET02_TYPE = 1

    spriteSheet = [None] * BULLET_TYPE_NUM
    imgs = [[] for n in range(BULLET_TYPE_NUM)]

    def __init__(self, owner, x, y, scrW, scrH, objType, dx, dy, speed=4.0):
        super(Bullet, self).__init__(x, y)
        self.__objType = objType
        self.__curFrameIndex = 0
        self.__scrW = scrW
        self.__scrH = scrH
        self.dx = dx * speed
        self.dy = dy * speed
        self.__rect = None
        for i in range(BULLET_TYPE_NUM):
            if not Bullet.spriteSheet[i]:
                Bullet.spriteSheet[i] = SpriteSheet("res/img/bullet%02d.png" %
                                                    (i + 1))

        if not Bullet.imgs[objType]:
            for frames in bulletsFrames[objType]:
                Bullet.imgs[objType].append(Bullet.spriteSheet[objType].
                                            getFrame(*frames))
        self.__animTimer = pygame.time.get_ticks()
        self.reset()
        # Bullet should belong to an owner. This helps to identify the owner
        # of the bullet and award the score to the bullet's owner when the
        # bullet hit and destroy the target object.
        self.setOwner(owner)

    def reset(self):
        self.state = Bullet.ALIVE
        self.__curFrameIndex = 0
        self.setFrame(0)

    def setOwner(self, owner):
        self.__owner = owner

    def getOwner(self):
        return self.__owner

    def setMovement(self, dx, dy, speed):
        self.dx, self.dy = (dx * speed, dy * speed)

    def setFrame(self, frameIndex):
        self.__img = (Bullet.imgs[self.__objType])[frameIndex]
        self.__rect = self.__img.get_rect()
        self.setPos(self.x, self.y)

    def setPos(self, x, y):
        self.__rect.centerx = int(x)
        self.__rect.centery = int(y)
        super(Bullet, self).setPos(x, y)

    def update(self):
        if self.state != Bullet.ALIVE:
            # Render small explosion if the bullet hit the target object
            if self.state == Bullet.EXPLODE:
                self.animate()
            return

        # Remove itself from game scene if its position is out of screen
        if self.__rect.left >= self.__scrW or \
           self.__rect.right <= 0 or \
           self.__rect.top >= self.__scrH or \
           self.__rect.bottom <= 0:
            self.state = Bullet.WASTED
            return

        self.setPos(self.x + self.dx, self.y + self.dy)

    def render(self, surf):
        if self.state != Bullet.WASTED:
            surf.blit(self.__img, (self.__rect.x, self.__rect.y))

    def animate(self):
        if pygame.time.get_ticks() - self.__animTimer < 50:
            return
        self.setFrame(self.__curFrameIndex)
        self.__curFrameIndex += 1
        if self.__curFrameIndex == len(Bullet.imgs[self.__objType]):
            # Remove itself from game scene after the last frame of
            # small explosion.
            self.state = Bullet.WASTED
        self.__animTimer = pygame.time.get_ticks()

    def isExpired(self):
        return self.state == Bullet.WASTED

    def getRect(self):
        return self.__rect

    def getDamage(self):
        return bulletsDamages[self.__objType]

    def setExplosion(self):
        self.state = Bullet.EXPLODE
