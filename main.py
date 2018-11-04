import pygame
import audio
import inspect
import sys
import random
import time
import persistence
import gameoverscr
import titlescr
import rankingscr
from pygame.locals import *
import gameconfig as gConf
import gameinputs as gInps
from scenemanager import SceneManager
from spawnmanager import SpawnManager
import cockpitLEDHUD as cockpit
from hpbar import HPBar
from bmptext import BmpText

# 4 different game modes.
GAMEMENU = 0
GAMEPLAY = 1
GAMEOVER = 2
GAMERANK = 3

hpBar = None
gameMode = GAMEMENU
currentScore = 0
bmpScore = None
highScore = 0
bmpHighScore = None
LEDShowExplosion = False


def gameInit():
    global GAMESCR, sceneMan, spawnMan
    random.seed()
    # Init Pygame library.
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    pygame.display.set_caption("SPYShip v%s" % gConf.VERSION)
    # Init graphics.
    GAMESCR = pygame.display.set_mode((gConf.SCREEN_W, gConf.SCREEN_H),
                                      pygame.FULLSCREEN if gConf.FULLSCREEN
                                      else 0)
    pygame.mouse.set_visible(False)
    sceneMan = SceneManager()
    spawnMan = SpawnManager(sceneMan)
    audio.loadAudioFiles()


# Handle transition between different game modes.
def switchGameMode(nextGameMode):
    global gameMode, hpBar, currentScore, bmpScore, highScore, bmpHighScore, \
        LEDShowExplosion

    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

    if nextGameMode != GAMEOVER:
        # Remove all game objects on screen except space background.
        sceneMan.clear()
        spawnMan.clearObjsCount()

    if nextGameMode == GAMEMENU:
        titlescr.init(sceneMan)
    elif nextGameMode == GAMEPLAY:
        if gConf.MUSIC:
            pygame.mixer.music.set_volume(0.6)
            # Start and repeat background music.
            pygame.mixer.music.play(-1)
        LEDShowExplosion = False
        # Let the game begin with first wave (less enemies).
        spawnMan.startWave()
        currentScore = 0
        bmpScore = BmpText(gConf.SCREEN_W - 10, 21,
                           str(currentScore), BmpText.BIG_FNT,
                           BmpText.RIGHT_ALIGN)
        sceneMan.add(bmpScore, SceneManager.HUD_L)
        highScore = (persistence.gRankings[0])[0]
        bmpHighScore = BmpText(gConf.SCREEN_W // 2, 21,
                               "HI-" + str(highScore), BmpText.SMALL_FNT,
                               BmpText.CENTER_ALIGN)
        sceneMan.add(bmpHighScore, SceneManager.HUD_L)
        spawnMan.spawnPlayer(SpawnManager.PLAYER1_ID, gInps.inputs)
        hpBar = HPBar(10, 8, spawnMan.getPlayer().getHPPercent())
        sceneMan.add(hpBar, SceneManager.HUD_L)
    elif nextGameMode == GAMEOVER:
        gameoverscr.init(sceneMan, currentScore)
    elif nextGameMode == GAMERANK:
        rankingscr.init(sceneMan)

    if not LEDShowExplosion:
        cockpit.clear()
    gameMode = nextGameMode


# Main handler for game title and main menu.
def gameMenu():
    ret = titlescr.main()
    if ret == 1:
        switchGameMode(GAMEPLAY)
    elif ret == 2:
        switchGameMode(GAMERANK)
    elif ret < 0:
        return -1
    return 0


# Main handler for actual game play.
def gamePlay():
    global currentScore, bmpScore, highScore, bmpHighScore, LEDShowExplosion

    if gameMode == GAMEPLAY:
        # Spawn enemies ?
        spawnMan.spawnEnemies()
        # Spawn power up ?
        spawnMan.spawnPowerUp()
        player = spawnMan.getPlayer()
        if player:
            # Update player's HP bar.
            hpBar.setBar(player.getHPPercent())
            if currentScore != player.score:
                currentScore = player.score
                # Update player's score.
                bmpScore.setText(str(currentScore))
                # If player beats the highest score
                if currentScore > highScore:
                    highScore = currentScore
                    # Update high score.
                    bmpHighScore.setText("HI-" + str(highScore))
            if not LEDShowExplosion and player.getHPPercent() <= 0:
                # Display explosion on Sense HAT LED matrix.
                LEDShowExplosion = True
                cockpit.resetExplosion()
        else:   # Switch to 'Game Over' mode if player is no longer 'exist'.
            hpBar.setBar(0.0)
            switchGameMode(GAMEOVER)
    elif gameMode == GAMEOVER:
        if gameoverscr.main():
            switchGameMode(GAMEMENU)


# Main game loop which keep the game running.
def gameLoop():
    global gameMode, LEDShowExplosion

    isDone = False
    getInputsTimer = pygame.time.get_ticks()
    LEDExplosionAnimTimer = pygame.time.get_ticks()

    clock = pygame.time.Clock()
    switchGameMode(GAMEMENU)
    # Game loop start here
    while not isDone:
        clock.tick(gConf.GAMESPEED)
        spawnMan.spawnAsteroid()

        if gameMode == GAMEMENU:
            if gameMenu() < 0:
                isDone = True
        elif gameMode == GAMEPLAY or gameMode == GAMEOVER:
            gamePlay()
        elif gameMode == GAMERANK:
            if rankingscr.main() < 0:
                switchGameMode(GAMEMENU)

        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            if gameMode == GAMEPLAY or gameMode == GAMEOVER or \
               gameMode == GAMERANK:
                switchGameMode(GAMEMENU)
        elif gConf.INPUT_CONTROLLER == gConf.INPUT_KEYBOARD:
            # Read keyboard inputs.
            gInps.mapKeys(keys)

        if gConf.INPUT_CONTROLLER == gConf.INPUT_SENSEHAT:
            if gameMode != GAMEPLAY:
                if pygame.time.get_ticks() - getInputsTimer > 33:
                    # Read Sense HAT inputs.
                    gInps.getSenseInputs(gInps.SENSE_STICK_INPUT)
                    getInputsTimer = pygame.time.get_ticks()
            elif not LEDShowExplosion:
                if pygame.time.get_ticks() - getInputsTimer > 100:
                    # Read Sense HAT gyroscope inputs.
                    gInps.getSenseInputs(gInps.SENSE_GYRO_INPUT)
                    # Update the Sense HAT LED matrix.
                    cockpit.showOrientation(gInps.inputs['r'] -
                                            gInps.inputs['l'],
                                            gInps.inputs['d'] -
                                            gInps.inputs['u'])
                    getInputsTimer = pygame.time.get_ticks()
            if LEDShowExplosion:
                if pygame.time.get_ticks() - LEDExplosionAnimTimer > 50:
                    LEDShowExplosion = not cockpit.showExplosion()
                    LEDExplosionAnimTimer = pygame.time.get_ticks()
        # Update game objects's state and position.
        sceneMan.update()
        # Render the game objects or sprites on screen.
        sceneMan.render(GAMESCR)
        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                isDone = True


def main():
    # Game initialization.
    gameInit()
    # Start game loop
    gameLoop()


# Main entry point.
if __name__ == '__main__':
    try:
        main()
    except SyntaxError as err:
        print(err)
    except Exception as exc:
        frm = inspect.trace()
        if frm:
            print(frm[-1][1])
        print(exc)

    # Clear Sense HAT LED matrix.
    cockpit.clear()
    # Save game settings into storage.
    persistence.saveSettings()
    # Save player's scores/rankings into storage.
    persistence.saveRankings()
    pygame.mixer.quit
    pygame.quit()
    sys.exit()
