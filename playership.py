import pygame
import random
import audio
from spritesheet import SpriteSheet
from shipobj import ShipObj
from bullet import Bullet
from explosion import Explosion
from shipfire import ShipFire

PLAYER_HP_MAX = 100

SHIPFRAME_NUM = 7
# Coordinates for player's ship animation frames
shipFrames = [
                (0, 0, 37, 24),
                (38, 0, 37, 23),
                (76, 0, 37, 22),
                (114, 1, 37, 21),
                (152, 1, 37, 24),
                (190, 1, 37, 25),
                (228, 2, 37, 24)
            ]

# Anim frames from top to bottom
shipStartFrame = SHIPFRAME_NUM // 2
shipAnimFrames = [3, 2, 1, 0, 4, 5, 6]

# Y offsets for jet's fire
fireFramesOffY = [1, 0, 0, 0, -1, -1, -2]

# Coordinates for protection shield animation frames
shieldFrames = [
                    (0, 0, 42, 42),
                    (43, 0, 42, 42),
                    (86, 0, 42, 42),
                    (129, 0, 42, 42),
                    (172, 0, 42, 42),
                    (215, 0, 42, 42)
            ]

"""
PlayerShip Class
----------------
Spaceship controlled by player
"""


class PlayerShip(ShipObj):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

    movStep = 1.5

    shipSpriteSheet = None
    shipImgFrames = []

    shieldSpriteSheet = None
    shieldImgFrames = []

    def __init__(self, spawn, inputs, x, y, scrW, scrH, shipID, isHitable,
                 godMode):
        super(PlayerShip, self).__init__(spawn, isHitable, shipID, godMode)
        self.shipID = shipID
        self.__explosion = Explosion(0, 0, Explosion.EXPLOSION01_TYPE)
        self.__fire = ShipFire(0, 0, ShipFire.SHIPFIRE01_TYPE)
        self.state = PlayerShip.ALIVE
        self.HP = PLAYER_HP_MAX
        self.__lastBtnReleased = False
        self.__isShooting = False
        self.__isShielded = False
        self.__shipImgFrames = []
        self.__curShipFrameIndex = shipStartFrame
        self.__curShieldFrameIndex = 0
        self.__scrW = scrW
        self.__scrH = scrH
        self.__inputs = inputs
        self.__shipRect = None

        if not PlayerShip.shieldSpriteSheet:
            PlayerShip.shieldSpriteSheet = SpriteSheet(
                "res/img/playershield.png")
        if not PlayerShip.shieldImgFrames:
            for frames in shieldFrames:
                PlayerShip.shieldImgFrames.append(PlayerShip.shieldSpriteSheet.
                                                  getFrame(*frames))

        if not PlayerShip.shipSpriteSheet:
            PlayerShip.shipSpriteSheet = SpriteSheet("res/img/playership.png")
        if not PlayerShip.shipImgFrames:
            for frames in shipFrames:
                PlayerShip.shipImgFrames.append(PlayerShip.shipSpriteSheet.
                                                getFrame(*frames))
        self.__shieldRect = PlayerShip.shieldImgFrames[0].get_rect()
        self.setShipFrame(shipAnimFrames[shipStartFrame])
        self.setPos(x, y)
        self.__shipAnimTimer = pygame.time.get_ticks()
        self.__shieldAnimTimer = pygame.time.get_ticks()
        self.__shootingTimer = pygame.time.get_ticks()
        self.setupBulletPool(Bullet.BULLET01_TYPE, scrW, scrH, 20)

    def setShipFrame(self, frameIndex):
        self.__shipImg = PlayerShip.shipImgFrames[frameIndex]
        self.__shipRect = self.__shipImg.get_rect()

    def setPos(self, x, y):
        self.__shipRect.centerx = int(x)
        self.__shipRect.centery = int(y)
        self.__shieldRect.centerx = int(x)
        self.__shieldRect.centery = int(y)
        self.__fire.setPos(self.__shipRect.left -
                           (self.__fire.getRect().width // 2),
                           self.__shipRect.centery +
                           fireFramesOffY[self.__curShipFrameIndex])
        super(PlayerShip, self).setPos(x, y)

    def update(self):
        if self.state != PlayerShip.ALIVE:
            if self.state == PlayerShip.EXPLODE:
                if not self.__explosion.isExpired():
                    self.__explosion.update()
                else:
                    self.state = PlayerShip.WASTED
            return

        if self.__inputs['l'] and self.__shipRect.left > 14:
            self.x -= (PlayerShip.movStep * self.__inputs['l'])
        elif self.__inputs['r'] and self.__shipRect.right <= self.__scrW:
            self.x += (PlayerShip.movStep * self.__inputs['r'])
        if self.__inputs['u'] and self.__shipRect.top >= 50:
            self.y -= (PlayerShip.movStep * self.__inputs['u'])
        elif self.__inputs['d'] and self.__shipRect.bottom <= self.__scrH:
            self.y += (PlayerShip.movStep * self.__inputs['d'])

        self.animateShip()
        self.__fire.update()
        self.setPos(self.x, self.y)
        self.shoot()

    def render(self, surf):
        if self.state == PlayerShip.ALIVE:
            self.__fire.render(surf)
            surf.blit(self.__shipImg, (self.__shipRect.x, self.__shipRect.y))
            # Show shield protection
            if self.godMode or self.__isShielded:
                surf.blit(PlayerShip.
                          shieldImgFrames[self.__curShieldFrameIndex],
                          (self.__shieldRect.x, self.__shieldRect.y))
        elif self.state == PlayerShip.EXPLODE:
            self.__explosion.render(surf)

    def animateShip(self):
        if pygame.time.get_ticks() - self.__shieldAnimTimer > 40:
            self.__curShieldFrameIndex += 1
            self.__curShieldFrameIndex %= len(PlayerShip.shieldImgFrames)
            self.__shieldAnimTimer = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.__shipAnimTimer > 100:
            up = self.__inputs['u']
            dn = self.__inputs['d']
            if up > 0:
                self.__curShipFrameIndex = shipStartFrame - \
                    int(up * shipStartFrame)
            elif dn > 0:
                self.__curShipFrameIndex = shipStartFrame + \
                    int(dn * shipStartFrame)
            else:
                self.__curShipFrameIndex = shipStartFrame
            self.setShipFrame(shipAnimFrames[self.__curShipFrameIndex])
            self.__shipAnimTimer = pygame.time.get_ticks()

    def shoot(self):
        # Toggle shooting
        if not self.__inputs['b']:
            self.__lastBtnReleased = True
        elif self.__lastBtnReleased:
            self.__isShooting = not self.__isShooting
            self.__lastBtnReleased = False

        if self.__isShooting:
            if pygame.time.get_ticks() - self.__shootingTimer > 120:
                bullet = self.getBulletFromPool()
                if bullet:
                    if not random.randint(0, 1):
                        audio.playSoundEffect('pshoot.wav')
                    bullet.setPos(self.__shipRect.right + 3,
                                  self.__shipRect.centery + 4)
                    PlayerShip.spawnMan.addPlayerBullet(bullet)
                    self.__shootingTimer = pygame.time.get_ticks()

    def isExpired(self):
        return self.state == PlayerShip.WASTED

    def isCollide(self, obj):
        if not self.isHitable or self.state != PlayerShip.ALIVE or \
           obj.state != Bullet.ALIVE:
            return False
        if self.getRect().colliderect(obj.getRect()):
            self.updateHP(obj.getDamage())
            expObj = Explosion(obj.x, obj.y, Explosion.EXPLOSION02_TYPE)
            PlayerShip.spawnMan.spawnPlayerDamage(expObj)
            audio.playSoundEffect('hit.wav')
            obj.setExplosion()
            return self.HP <= 0
        return False

    def getRect(self):
        return self.__shipRect

    def getDamage(self):
        return -1000

    def setExplosion(self):
        self.state = PlayerShip.EXPLODE
        self.__explosion.setPos(self.x, self.y)
        audio.playSoundEffect('pexp.wav')

    def getReward(self):
        return 0

    def updateHP(self, p):
        # Prevent damage if player is in god mode
        if p < 0 and self.godMode:
            return
        # Prevent damage and remove shield protection
        if p < 0 and self.__isShielded:
            self.__isShielded = False
            return
        self.HP += p
        # Enable shield protection if player's health point is overflow
        if self.HP > PLAYER_HP_MAX:
            self.HP = PLAYER_HP_MAX
            self.__isShielded = True
        elif self.HP <= 0:  # Take damage and show explosion if run out of HP
            self.HP = 0
            self.setExplosion()

    def getHPPercent(self):
        return self.HP / PLAYER_HP_MAX
