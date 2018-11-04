import pygame
import gameconfig as gConf

# Dictionary for storing preloaded sound effects
# Key: Filename of the sound effect
# Value: Audio data
_sndLib = {}


def loadSoundEffect(file):
    global _sndLib

    snd = _sndLib.get(file)
    if not snd:
        path = 'res/audio/%s' % file
        snd = pygame.mixer.Sound(path)
        _sndLib[file] = snd
    return snd


def playSoundEffect(file):
    global _sndLib

    if not gConf.SOUND:
        return

    snd = _sndLib.get(file)
    # Load the sound effect if it was not loaded before
    if not snd:
        snd = loadSoundEffect(file)
    snd.play()


def loadAllSoundEffects():
    # Preload all the sound effects
    loadSoundEffect('hit.wav')
    loadSoundEffect('beep.wav')
    loadSoundEffect('done.wav')
    loadSoundEffect('pshoot.wav')
    loadSoundEffect('eexp.wav')
    loadSoundEffect('pexp.wav')
    loadSoundEffect('bexp.wav')
    loadSoundEffect('hppowerup.wav')
    loadSoundEffect('gamestart.ogg')
    loadSoundEffect('gameover.wav')


def loadBGMusic():
    # Preload background music
    pygame.mixer.music.load('res/audio/bgmusicloop.wav')


def loadAudioFiles():
    # Preload soud effects and background music
    loadBGMusic()
    loadAllSoundEffects()


def toggleMusic():
    gConf.MUSIC = not gConf.MUSIC
    return gConf.MUSIC


def toggleSound():
    gConf.SOUND = not gConf.SOUND
    return gConf.SOUND
