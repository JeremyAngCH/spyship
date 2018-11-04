import pygame
import random
from asteroid import Asteroid
import gameconfig as gConf
from scenemanager import SceneManager
from spacebg import SpaceBG
from playership import PlayerShip
from enemy01 import Enemy01
from enemy02 import Enemy02
from enemy03 import Enemy03
from enemy04 import Enemy04
from enemy05 import Enemy05
from powerup import PowerUp


ENEMY1_MAX_NUM = 5
ENEMY2_MAX_NUM = 4
ENEMY3_MAX_NUM = 4
ENEMY_SPAWN_INTERVALS_MS = 250
ENEMY_BOSSSPAWN_COOLDOWN_MS = 120000
ENEMY_HIGHLEVELSPAWN_COOLDOWN_MS = 30000
POWERUP_SPAWN_COOLDOWN_MS = 45000

# There are total 8 waves. More enemies including advanced enemies will
# appear as the wave advances after a specified amount of time as defined
# in WAVE_INTERVAL_MS.
WAVE_INTERVAL_MS = 15000
WAVE_MAX = 8

"""
SpawnManager Class
------------------
A Singleton class.
This class manages and controls the difficulty and pace of the game play.
It creates game objects and add them into game scene via SceneManager.
"""


class SpawnManager:
    PLAYER1_ID = 0
    ENEMY1_ID = (PLAYER1_ID + 1)
    ENEMY2_ID = (ENEMY1_ID + 1)
    ENEMY3_ID = (ENEMY2_ID + 1)
    ENEMY4_ID = (ENEMY3_ID + 1)
    ENEMY5_ID = (ENEMY4_ID + 1)
    MAX_ID = (ENEMY5_ID + 1)

    objsCount = [0] * MAX_ID
    wave = 0
    wave_interval_ms = WAVE_INTERVAL_MS

    class __SpawnManager:

        def __init__(self, sceneManager):
            self.__player = None
            self.__asteroidTimer = pygame.time.get_ticks()
            self.__sceneMan = sceneManager
            self.__sceneMan.add(SpaceBG(gConf.SCREEN_W, gConf.SCREEN_H),
                                SceneManager.ASTEROID_L)
            self.startWave()

        def clearObjsCount(self):
            for i in range(SpawnManager.MAX_ID):
                SpawnManager.objsCount[i] = 0

        def updateObjsCount(self, objID, count):
            SpawnManager.objsCount[objID] += count

        # Game begin from first wave.
        def startWave(self):
            SpawnManager.wave = 0
            SpawnManager.wave_interval_ms = WAVE_INTERVAL_MS
            self.__spawnEnemyTimer = pygame.time.get_ticks()
            self.__lowLevelLastSeenTimer = pygame.time.get_ticks()
            self.__highLevelLastSpawnTimer = pygame.time.get_ticks()
            self.__bossLastSpawnTimer = pygame.time.get_ticks()
            self.__powerUpLastSpawnTimer = pygame.time.get_ticks()
            self.__powerUpNextCoolDownPeriod = POWERUP_SPAWN_COOLDOWN_MS + \
                random.randint(0, 5) * 10000

        # Advance waves after a specified amount of time (WAVE_INTERVAL_MS).
        def updateWave(self):
            SpawnManager.wave_interval_ms -= ENEMY_SPAWN_INTERVALS_MS
            if not SpawnManager.wave_interval_ms:
                SpawnManager.wave_interval_ms = WAVE_INTERVAL_MS
                if SpawnManager.wave < WAVE_MAX:
                    SpawnManager.wave += 1

        def spawnAsteroid(self):
            if pygame.time.get_ticks() - self.__asteroidTimer > 2500:
                asteroid = Asteroid(0, 0, -random.uniform(0.4, 0.7),
                                    random.randint(Asteroid.GREY,
                                                   Asteroid.BROWN))
                asteroid.setPos(gConf.SCREEN_W + asteroid.rect.width,
                                random.randint(0, (gConf.SCREEN_H / 1.5) //
                                               (asteroid.rect.height // 2)) *
                                asteroid.rect.height)
                self.__sceneMan.add(asteroid, SceneManager.ASTEROID_L)
                self.__asteroidTimer = pygame.time.get_ticks()

        def addPlayerBullet(self, bullet):
            self.__sceneMan.add(bullet, SceneManager.PBULLET_L)

        def addEnemyBullet(self, bullet):
            self.__sceneMan.add(bullet, SceneManager.EBULLET_L)

        def getPlayer(self):
            if not self.__player:
                return None
            elif self.__player.isUnused() or self.__player.isExpired():
                self.__player = None
            return self.__player

        def spawnPlayer(self, shipID, inputs):
            self.__player = PlayerShip(self, inputs, (gConf.SCREEN_W / 4),
                                       gConf.CENTER_Y, gConf.SCREEN_W,
                                       gConf.SCREEN_H, shipID, True,
                                       gConf.GODMODE)
            self.updateObjsCount(shipID, 1)
            self.__sceneMan.add(self.__player, SceneManager.PLAYER_L)

        def spawnPlayerDamage(self, expObj):
            self.__sceneMan.add(expObj, SceneManager.EFFECTS_L)

        def __spawnLowLevelEnemy(self):
            n = random.randint(1, 1 + (SpawnManager.wave // 3))
            if SpawnManager.objsCount[SpawnManager.ENEMY4_ID]:
                r = random.randint(0, 2)
                if r >= 1:
                    n = 1
                else:
                    n = 0

            for i in range(n):
                enemyShip = None
                if SpawnManager.objsCount[SpawnManager.ENEMY5_ID]:
                    if not random.randint(0, 7):
                        shipType = 6
                    else:
                        return
                else:
                    shipType = random.randint(0, 6)
                if shipType < 3:
                    if SpawnManager.objsCount[SpawnManager.ENEMY1_ID] < \
                       ENEMY1_MAX_NUM:
                        enemyShip = Enemy01(self, gConf.SCREEN_W + 100,
                                            random.randint(20,
                                                           gConf.SCREEN_H - 5),
                                            gConf.SCREEN_W, gConf.SCREEN_H,
                                            SpawnManager.ENEMY1_ID, True)
                        self.__sceneMan.add(enemyShip, SceneManager.ENEMYM_L)
                elif shipType >= 3 and shipType < 6:
                    if SpawnManager.objsCount[SpawnManager.ENEMY2_ID] < \
                       ENEMY2_MAX_NUM:
                        enemyShip = Enemy02(self, gConf.SCREEN_W + 100,
                                            random.randint(20,
                                                           gConf.SCREEN_H - 5),
                                            gConf.SCREEN_W,
                                            gConf.SCREEN_H,
                                            SpawnManager.ENEMY2_ID, True)
                        self.__sceneMan.add(enemyShip, SceneManager.ENEMYM_L)
                elif SpawnManager.wave >= 3:
                    randY = random.randint(50, gConf.SCREEN_H - 20)
                    for ph in range(2):
                        if SpawnManager.objsCount[SpawnManager.ENEMY3_ID] < \
                           ENEMY3_MAX_NUM:
                            enemyShip = Enemy03(self, gConf.SCREEN_W + 100,
                                                randY, gConf.SCREEN_W,
                                                gConf.SCREEN_H,
                                                SpawnManager.ENEMY3_ID,
                                                True, ph)
                            self.__sceneMan.add(enemyShip,
                                                SceneManager.ENEMYF_L)
                            self.updateObjsCount(enemyShip.shipID, 1)
                    enemyShip = None

                if enemyShip:
                    self.updateObjsCount(enemyShip.shipID, 1)

        def __spawnHighLevelEnemy(self):
            if SpawnManager.objsCount[SpawnManager.ENEMY4_ID] or \
               SpawnManager.objsCount[SpawnManager.ENEMY5_ID]:
                return
            enemyShip = Enemy04(self, gConf.SCREEN_W + 100,
                                random.randint(20, gConf.SCREEN_H - 5),
                                gConf.SCREEN_W, gConf.SCREEN_H,
                                SpawnManager.ENEMY4_ID, True)
            self.__sceneMan.add(enemyShip, SceneManager.ENEMYB_L)
            self.updateObjsCount(enemyShip.shipID, 1)

        def __spawnBossEnemy(self):
            if SpawnManager.objsCount[SpawnManager.ENEMY4_ID] or \
               SpawnManager.objsCount[SpawnManager.ENEMY5_ID]:
                return
            enemyShip = Enemy05(self, gConf.SCREEN_W + 100,
                                random.randint(20, gConf.SCREEN_H - 5),
                                gConf.SCREEN_W, gConf.SCREEN_H,
                                SpawnManager.ENEMY5_ID, True)
            self.__sceneMan.add(enemyShip, SceneManager.ENEMYB_L)
            self.updateObjsCount(enemyShip.shipID, 1)
            self.__bossLastSpawnTimer = pygame.time.get_ticks()

        # Spawn more and more enemies as the wave advances
        def spawnEnemies(self):
            if pygame.time.get_ticks() - self.__spawnEnemyTimer < \
               ENEMY_SPAWN_INTERVALS_MS:
                return

            if SpawnManager.objsCount[SpawnManager.ENEMY5_ID]:
                self.__bossLastSpawnTimer = pygame.time.get_ticks()

            if (SpawnManager.objsCount[SpawnManager.ENEMY1_ID] +
                SpawnManager.objsCount[SpawnManager.ENEMY2_ID] +
                    SpawnManager.objsCount[SpawnManager.ENEMY3_ID]) > 0:
                self.__lowLevelLastSeenTimer = pygame.time.get_ticks()

            self.updateWave()

            if pygame.time.get_ticks() - self.__lowLevelLastSeenTimer > \
               1500:
                self.__spawnLowLevelEnemy()
            elif random.randint(0, ((WAVE_MAX + 1) - SpawnManager.wave) * 2) \
                == 0 or (SpawnManager.wave <= 2 and
                         random.randint(0, 10) == 0):
                self.__spawnLowLevelEnemy()
            elif SpawnManager.wave >= 4 and \
                pygame.time.get_ticks() - self.__highLevelLastSpawnTimer > \
                    ENEMY_HIGHLEVELSPAWN_COOLDOWN_MS:
                if random.randint(0, 1):
                    self.__spawnHighLevelEnemy()
                self.__highLevelLastSpawnTimer = pygame.time.get_ticks()
            elif SpawnManager.wave >= WAVE_MAX and \
                pygame.time.get_ticks() - self.__bossLastSpawnTimer > \
                    ENEMY_BOSSSPAWN_COOLDOWN_MS:
                self.__spawnBossEnemy()

            self.__spawnEnemyTimer = pygame.time.get_ticks()

        def spawnPowerUp(self):
            if pygame.time.get_ticks() - self.__powerUpLastSpawnTimer > \
               self.__powerUpNextCoolDownPeriod:
                self.__powerUpLastSpawnTimer = pygame.time.get_ticks()
                if random.randint(0, 1):
                    return
                powerUp = PowerUp(gConf.SCREEN_W + 100,
                                  random.randint(20,
                                                 gConf.SCREEN_H - 5),
                                  gConf.SCREEN_W, gConf.SCREEN_H,
                                  PowerUp.POWERUP01_TYPE)
                self.__sceneMan.add(powerUp, SceneManager.POWERUP_L)
                self.__powerUpNextCoolDownPeriod = POWERUP_SPAWN_COOLDOWN_MS \
                    + random.randint(0, 5) * 10000

    __inst = None

    def __init__(self, sceneManager):
        if not SpawnManager.__inst:
            SpawnManager.__inst = SpawnManager.__SpawnManager(sceneManager)

    def __getattr__(self, name):
        return getattr(self.__inst, name)
