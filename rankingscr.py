import pygame
import persistence
import gameinputs as gInps
import gameconfig as gConf
from scenemanager import SceneManager
from bmptext import BmpText
from imgobj import ImgObj

RANK_MAX_ROW = 11

__xRatio = [0.1765, 0.5, 0.8235]
__rankDesc = ["RANK", "SCORE", "NAME"]
__rankInfo = []
__sceneMan = None
__highScoresImg = None
__rankDisplayTimer = 0
__currentRankIndex = 0
__currentYRatio = 0


def appendRankSuffix(rank):
    if rank == 0:
        return "st"
    elif rank == 1:
        return "nd"
    elif rank == 2:
        return "rd"
    return "th"


def loadRankInfo():
    global __rankInfo

    __rankInfo.clear()
    for i in range(RANK_MAX_ROW - 1):
        info = []
        rankStr = str(i + 1) + appendRankSuffix(i)
        info.append(rankStr)
        info.append(str((persistence.gRankings[i])[0]))
        info.append((persistence.gRankings[i])[1])
        __rankInfo.append(info)


def init(sceneMan):
    global __sceneMan, __highScoresImg, __currentRankIndex, \
           __rankDisplayTimer, __currentYRatio

    __sceneMan = sceneMan
    __highScoresImg = ImgObj(gConf.SCREEN_W // 2, gConf.SCREEN_H * 0.1145,
                             'res/img/highscores.png', ImgObj.TOP_STYLE)
    __sceneMan.add(__highScoresImg, SceneManager.MENU_L)
    __rankDisplayTimer = pygame.time.get_ticks()
    __currentYRatio = 0.3375
    __currentRankIndex = 0
    loadRankInfo()


# Display player's 10 best scores one at a time in each function call
def main():
    global __highScoresImg, __currentRankIndex, __rankDisplayTimer, \
           __currentYRatio

    if not __highScoresImg.isAnimating():
        if gInps.isButtonHit():
            return -1

        if __currentRankIndex <= (RANK_MAX_ROW - 1) and \
           pygame.time.get_ticks() - __rankDisplayTimer > 100:
            if __currentRankIndex == 0:
                for i in range(len(__rankDesc)):
                    bmpText = BmpText(gConf.SCREEN_W * __xRatio[i],
                                      gConf.SCREEN_H * 0.25,
                                      __rankDesc[i], BmpText.BIG_FNT,
                                      BmpText.CENTER_ALIGN)
                    __sceneMan.add(bmpText, SceneManager.MENU_L)
            else:
                for i in range(len(__rankDesc)):
                    align = BmpText.CENTER_ALIGN
                    xr = __xRatio[i]
                    if i == 1:
                        align = BmpText.RIGHT_ALIGN
                        xr = 0.5825
                    bmpText = BmpText(gConf.SCREEN_W * xr,
                                      gConf.SCREEN_H * __currentYRatio,
                                      (__rankInfo[__currentRankIndex - 1])[i],
                                      BmpText.SMALL_FNT, align)
                    __sceneMan.add(bmpText, SceneManager.MENU_L)
                __currentYRatio += 0.0666

            __currentRankIndex += 1
            __rankDisplayTimer = pygame.time.get_ticks()

    return 0
