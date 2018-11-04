"""
SceneManager Class
------------------
A Singleton class.
Manage sprites update, collision checks and sprites rendering order.
"""


class SceneManager:
    # Rendering order: Larger number get rendered first on screen
    # MENU_L is the lowest number and top most layer which covers other layers
    MENU_L = 0
    HUD_L = MENU_L + 1
    EFFECTS_L = HUD_L + 1
    EBULLET_L = EFFECTS_L + 1
    PBULLET_L = EBULLET_L + 1
    POWERUP_L = PBULLET_L + 1
    ENEMYF_L = POWERUP_L + 1
    ENEMYM_L = ENEMYF_L + 1
    ENEMYB_L = ENEMYM_L + 1
    PLAYER_L = ENEMYB_L + 1
    ASTEROID_L = PLAYER_L + 1
    MAX_LAYER = ASTEROID_L

    class __SceneManager:

        def __init__(self):
            self.__layers = [[] for l in range(SceneManager.MAX_LAYER + 1)]

        # Add sprite to layer
        def add(self, obj, layer=0):
            self.__layers[layer].append(obj)

        # Remove all sprites in each layer except ASTEROID_L
        def clear(self):
            for n in range(SceneManager.MAX_LAYER):
                del (self.__layers[n])[:]

        # Update sprites in each layer
        def update(self):
            for n in reversed(range(SceneManager.MAX_LAYER + 1)):
                objs = self.__layers[n]
                objCnt = len(objs)
                for i in reversed(range(objCnt)):
                    objs[i].update()
                    # Sprites no longer active. Remove from screen.
                    if objs[i].isExpired():
                        objs[i].setUnused()
                        del objs[i]
            self.checkCollision()

        # Render sprites from layer ASTEROID_L to layer MENU_L
        def render(self, surf):
            for n in reversed(range(SceneManager.MAX_LAYER + 1)):
                objs = self.__layers[n]
                for obj in objs:
                    if obj.visible:
                        obj.render(surf)

        def checkCollision(self):
            for n in range(SceneManager.ENEMYF_L, SceneManager.ENEMYB_L + 1):
                objs = self.__layers[n]
                objCnt = len(objs)
                # check player collision with enemies
                for p in self.__layers[SceneManager.PLAYER_L]:
                    for i in reversed(range(objCnt)):
                        if objs[i].isCollide(p):
                            break
                # check player's bullet collision with enemies
                for b in self.__layers[SceneManager.PBULLET_L]:
                    for i in reversed(range(objCnt)):
                        if objs[i].isCollide(b):
                            break

            # check enemies's bullet collision with player
            for p in self.__layers[SceneManager.PLAYER_L]:
                for b in self.__layers[SceneManager.EBULLET_L]:
                    if p.isCollide(b):
                        break

            # check power-up collision with player
            for u in self.__layers[SceneManager.POWERUP_L]:
                for p in self.__layers[SceneManager.PLAYER_L]:
                    if u.isCollide(p):
                        break

    __inst = None

    def __init__(self):
        if not SceneManager.__inst:
            SceneManager.__inst = SceneManager.__SceneManager()

    def __getattr__(self, name):
        return getattr(self.__inst, name)
