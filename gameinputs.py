import os
from pygame.locals import *
import gameconfig as gConf

if gConf.INPUT_CONTROLLER == gConf.INPUT_SENSEHAT:
    from sense_hat import SenseHat

SENSE_GYRO_INPUT = 0
SENSE_STICK_INPUT = 1

# Set the origin of the gyroscope in degree of angle
LR_DEGREE_ORIGIN = 0
UD_DEGREE_ORIGIN = 20
DEGREE_MAX = 20.0

sense = None
try:
    if gConf.INPUT_CONTROLLER == gConf.INPUT_SENSEHAT:
        sense = SenseHat()
except Exception as exc:
    print("%s: %s" %
          (os.path.splitext(os.path.basename(__file__))[0], exc))

# 'l' = LEFT, 'r' = RIGHT, 'u' = UP, 'd' = DOWN, 'b' = SELECT/SHOOT
# Direction inputs have magnitude ranging from 0 to 1.0
inputs = {'l': 0.0, 'r': 0.0, 'u': 0.0, 'd': 0.0, 'b': False}
wasButtonHit = False


def resetInputDirections():
    global inputs
    for k in inputs:
        if k != 'b':
            inputs[k] = 0.0


def getSenseInputs(inputMode):
    global sense, inputs

    if not sense:
        return

    resetInputDirections()

    # Keep reading the gyroscope to make sure we always get the latest value
    orientation = sense.get_orientation_degrees()
    # Gyroscope has magnitude ranging from 0 to 1.0 depending
    # on its angle.
    if inputMode == SENSE_GYRO_INPUT:
        lr = int(orientation['pitch'])
        if lr >= LR_DEGREE_ORIGIN and lr < (LR_DEGREE_ORIGIN + 180):
            d = (lr - LR_DEGREE_ORIGIN) / DEGREE_MAX
            inputs['l'] = 1.0 if d > 1.0 else d
        elif lr > 260 and lr < 360:
            d = (360 - lr) / DEGREE_MAX
            inputs['r'] = 1.0 if d > 1.0 else d
        ud = int(orientation['roll'])
        if ud > UD_DEGREE_ORIGIN and ud < (UD_DEGREE_ORIGIN + 180):
            d = (ud - UD_DEGREE_ORIGIN) / DEGREE_MAX
            inputs['u'] = 1.0 if d > 1.0 else d
        elif ud < UD_DEGREE_ORIGIN or ud > (UD_DEGREE_ORIGIN + 180):
            d = (UD_DEGREE_ORIGIN - ud) if ud < UD_DEGREE_ORIGIN else \
                UD_DEGREE_ORIGIN
            d += (360 - ud) if ud > (UD_DEGREE_ORIGIN + 180) else 0.0
            d /= DEGREE_MAX
            inputs['d'] = 1.0 if d > 1.0 else d

    # Direction stick on the Sense HAT only has magnitude of 0.0 and 1.0
    for event in sense.stick.get_events():
        if event.direction == 'middle':
            inputs['b'] = False if event.action == 'released' else True
        if inputMode == SENSE_STICK_INPUT:
            if event.direction == 'left':
                inputs['l'] = 0.0 if event.action == 'released' else 1.0
            elif event.direction == 'right':
                inputs['r'] = 0.0 if event.action == 'released' else 1.0
            elif event.direction == 'up':
                inputs['u'] = 0.0 if event.action == 'released' else 1.0
            elif event.direction == 'down':
                inputs['d'] = 0.0 if event.action == 'released' else 1.0
    return inputs


def mapKeys(keys):
    # Key press on computer keyboard only has magnitude of 0.0 and 1.0
    resetInputDirections()
    if keys[K_LEFT] or keys[K_a]:
        inputs['l'] = 1.0
    elif keys[K_RIGHT] or keys[K_d]:
        inputs['r'] = 1.0

    if keys[K_UP] or keys[K_w]:
        inputs['u'] = 1.0
    elif keys[K_DOWN] or keys[K_s]:
        inputs['d'] = 1.0

    inputs['b'] = True if keys[K_SPACE] or keys[K_RETURN] else False


def isButtonHit():
    global wasButtonHit

    if wasButtonHit != inputs['b']:
        wasButtonHit = inputs['b']
        if not inputs['b']:
            return True
    return False


def isButtonUp():
    if inputs['u']:
        return True
    return False


def isButtonDown():
    if inputs['d']:
        return True
    return False


def isButtonLeft():
    if inputs['l']:
        return True
    return False


def isButtonRight():
    if inputs['r']:
        return True
    return False
