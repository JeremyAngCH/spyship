import pygame
import audio
import persistence
import rankingscr
import gameinputs as gInps
import gameconfig as gConf
from scenemanager import SceneManager
from bmptext import BmpText
from imgobj import ImgObj

__sceneMan = None
__gameOverImg = None

NORMAL_STATE = 0
INPUTNAME_STATE = NORMAL_STATE + 1
DONE_STATE = INPUTNAME_STATE + 1

__state = NORMAL_STATE
__currentScore = 0
__currentInitialIndex = 0
__initialsImg = []

__inputDelayTimer = 0
__noKeyPressed = True


def init(sceneMan, score):
    global __sceneMan, __gameOverImg, __state, __currentScore

    __currentScore = score
    __state = NORMAL_STATE
    __sceneMan = sceneMan
    audio.playSoundEffect('gameover.wav')
    __gameOverImg = ImgObj(gConf.SCREEN_W // 2, gConf.SCREEN_H * 0.25,
                           'res/img/gameover.png', ImgObj.CENTER_STYLE)
    __sceneMan.add(__gameOverImg, SceneManager.MENU_L)
    __initialsImg.clear()


def main():
    global __gameOverImg, __state, __currentScore, __currentInitialIndex, \
           __noKeyPressed, __inputDelayTimer

    if __state == NORMAL_STATE:
        # Done rendering "Game Over"
        if not __gameOverImg.isAnimating():
            bmpText = None
            rank = persistence.checkRankings(__currentScore)
            if rank < 0:
                bmpText = BmpText(gConf.SCREEN_W // 2, gConf.SCREEN_H * 0.6,
                                  "PRESS A BUTTON TO RETURN TO MENU",
                                  BmpText.SMALL_FNT, BmpText.CENTER_ALIGN,
                                  True, True)
                __sceneMan.add(bmpText, SceneManager.MENU_L)
                __state = DONE_STATE
            else:
                # Player's score made it into the ten best scores
                bmpText = BmpText(gConf.SCREEN_W // 2, gConf.SCREEN_H * 0.5,
                                  "YOUR HIGH SCORE RANKING: " + str(rank + 1) +
                                  rankingscr.appendRankSuffix(rank),
                                  BmpText.SMALL_FNT, BmpText.CENTER_ALIGN)
                __sceneMan.add(bmpText, SceneManager.MENU_L)
                bmpText = BmpText(gConf.SCREEN_W // 2, gConf.SCREEN_H * 0.6,
                                  "ENTER YOUR INITIALS:", BmpText.SMALL_FNT,
                                  BmpText.CENTER_ALIGN)
                __sceneMan.add(bmpText, SceneManager.MENU_L)
                __state = INPUTNAME_STATE
                __currentInitialIndex = 0
                startX = (gConf.SCREEN_W // 2) - 32
                for i in range(4):
                    initialChars = 'A'
                    if i == 3:
                        initialChars = '_'  # Display 'END'
                    bmpText = BmpText(startX,
                                      gConf.SCREEN_H * 0.725,
                                      initialChars,
                                      BmpText.BIG_FNT, BmpText.CENTER_ALIGN)
                    __sceneMan.add(bmpText, SceneManager.MENU_L)
                    startX += 32
                    __initialsImg.append(bmpText)
                __initialsImg[0].setBlink(True)
                __noKeyPressed = True
                __inputDelayTimer = pygame.time.get_ticks()
    elif __state == INPUTNAME_STATE:
        if not(gInps.isButtonDown() or gInps.isButtonUp() or
               gInps.isButtonLeft() or gInps.isButtonRight()):
            __noKeyPressed = True

        if pygame.time.get_ticks() - __inputDelayTimer > 225 or \
           __noKeyPressed:
            if gInps.isButtonDown() or gInps.isButtonUp() or \
               gInps.isButtonLeft() or gInps.isButtonRight():
                __noKeyPressed = False
                if __currentInitialIndex == 3:
                    curChar = __initialsImg[__currentInitialIndex].getText()
                    if curChar == '_':
                        curChar = '^'
                    else:
                        curChar = '_'
                    __initialsImg[__currentInitialIndex].setText(curChar)

            if __currentInitialIndex < 3:
                if gInps.isButtonDown() or gInps.isButtonRight():
                    curChar = __initialsImg[__currentInitialIndex].getText()
                    if curChar == 'Z':
                        curChar = 'A'
                    else:
                        curChar = chr(ord(curChar) + 1)
                    __initialsImg[__currentInitialIndex].setText(curChar)
                elif gInps.isButtonUp() or gInps.isButtonLeft():
                    curChar = __initialsImg[__currentInitialIndex].getText()
                    if curChar == 'A':
                        curChar = 'Z'
                    else:
                        curChar = chr(ord(curChar) - 1)
                    __initialsImg[__currentInitialIndex].setText(curChar)
            __inputDelayTimer = pygame.time.get_ticks()

        if gInps.isButtonHit():
            __initialsImg[__currentInitialIndex].setBlink(False)
            # Confirm single initial
            if __currentInitialIndex < 3:
                __currentInitialIndex += 1
                __initialsImg[__currentInitialIndex].setBlink(True)
                audio.playSoundEffect('beep.wav')
            else:
                # Confirm initials
                curChar = __initialsImg[__currentInitialIndex].getText()
                if curChar == '_':  # END
                    name = ''
                    for i in range(3):
                        name += __initialsImg[i].getText()
                    bmpText = BmpText(gConf.SCREEN_W // 2,
                                      gConf.SCREEN_H * 0.875,
                                      "CONGRATULATIONS!", BmpText.SMALL_FNT,
                                      BmpText.CENTER_ALIGN, True, True)
                    __sceneMan.add(bmpText, SceneManager.MENU_L)
                    persistence.insertRankings(__currentScore, name)
                    __state = DONE_STATE
                    audio.playSoundEffect('done.wav')
                else:  # DEL
                    # Re-input initials
                    __initialsImg[__currentInitialIndex].setText('_')
                    __currentInitialIndex = 0
                    __initialsImg[__currentInitialIndex].setBlink(True)
                    audio.playSoundEffect('beep.wav')
    elif __state == DONE_STATE:
        if gInps.isButtonHit():
            return -1
    return 0
