import pygame
import audio
import gameinputs as gInps
import gameconfig as gConf
from scenemanager import SceneManager
from bmptext import BmpText
from imgobj import ImgObj

START_OPTION = 0
HIGHSCORES_OPTION = START_OPTION + 1
MUSIC_OPTION = HIGHSCORES_OPTION + 1
SOUND_OPTION = MUSIC_OPTION + 1
QUIT_OPTION = SOUND_OPTION + 1

__optionTexts = ["START GAME", "HIGH SCORES", "MUSIC", "SOUND", "QUIT GAME"]
__sceneMan = None
__titleImg = None
__selections = []
__currentSel = START_OPTION

__inputDelayTimer = 0
__noKeyPressed = True
__gameStarted = False


def appendSettings(text):
    if 'MUSIC' in text:
        text += " ON" if gConf.MUSIC else " OFF"
    elif 'SOUND' in text:
        text += " ON" if gConf.SOUND else " OFF"
    return text


def updateSelections():
    global __inputDelayTimer

    for i in range(len(__optionTexts)):
        if __currentSel == i:
            __selections[i].setFntType(BmpText.BIG_FNT)
        else:
            __selections[i].setFntType(BmpText.SMALL_FNT)


# Display game title and main menu.
def init(sceneMan):
    global __sceneMan, __titleImg, __selections, __gameStarted

    __sceneMan = sceneMan
    __titleImg = ImgObj(gConf.SCREEN_W // 2, gConf.SCREEN_H * 0.2645,
                        'res/img/title.png', ImgObj.TOP_STYLE)
    __sceneMan.add(__titleImg, SceneManager.MENU_L)

    if not __selections:
        yRatio = 0.4833
        for txt in __optionTexts:
            bmpText = BmpText(gConf.SCREEN_W // 2, gConf.SCREEN_H * yRatio,
                              appendSettings(txt), BmpText.SMALL_FNT,
                              BmpText.CENTER_ALIGN)
            __sceneMan.add(bmpText, SceneManager.MENU_L)
            __selections.append(bmpText)
            yRatio += 0.06875
    else:
        for i in range(len(__optionTexts)):
            __sceneMan.add(__selections[i], SceneManager.MENU_L)
    updateSelections()
    __gameStarted = False


# Handle main menu selection
def main():
    global __titleImg, __selections, __currentSel, __inputDelayTimer, \
           __noKeyPressed, __gameStarted

    if __gameStarted:
        if pygame.time.get_ticks() - __inputDelayTimer < 1200:
            return 0
        __selections[START_OPTION].setBlink(False)
        return 1

    if not __titleImg.isAnimating():
        if gInps.isButtonHit():
            if __currentSel == QUIT_OPTION:
                return -1
            elif __currentSel == START_OPTION:
                __gameStarted = True
                audio.playSoundEffect('gamestart.ogg')
                __selections[START_OPTION].setBlink(True)
                __inputDelayTimer = pygame.time.get_ticks()
                return 0
            elif __currentSel == HIGHSCORES_OPTION:
                return 2
            else:
                if __currentSel == MUSIC_OPTION:
                    audio.toggleMusic()
                elif __currentSel == SOUND_OPTION:
                    audio.toggleSound()
                text = appendSettings(__selections[__currentSel].getText().
                                      partition(' ')[0])
                __selections[__currentSel].setText(text)

        if not(gInps.isButtonDown() or gInps.isButtonUp() or
               gInps.isButtonLeft() or gInps.isButtonRight()):
            __noKeyPressed = True

        if pygame.time.get_ticks() - __inputDelayTimer > 200 or \
           __noKeyPressed:
            if gInps.isButtonDown() or gInps.isButtonUp() or \
               gInps.isButtonLeft() or gInps.isButtonRight():
                __noKeyPressed = False

            if gInps.isButtonDown():
                __currentSel += 1
                audio.playSoundEffect('beep.wav')
            elif gInps.isButtonUp():
                if __currentSel == 0:
                    __currentSel = len(__optionTexts) - 1
                else:
                    __currentSel -= 1
                audio.playSoundEffect('beep.wav')
            __currentSel = __currentSel % len(__optionTexts)
            updateSelections()
            __inputDelayTimer = pygame.time.get_ticks()
    return 0
