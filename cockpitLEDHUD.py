import pygame
import random
import os
import gameconfig as gConf

# Only import the Sense HAT module if the input controller is set as Sense HAT
if gConf.INPUT_CONTROLLER == gConf.INPUT_SENSEHAT:
    from sense_hat import SenseHat

sense = None
try:
    # Try to initialize the Sense HAT module
    if gConf.INPUT_CONTROLLER == gConf.INPUT_SENSEHAT:
        sense = SenseHat()
except Exception as exc:
    print("%s: %s" %
          (os.path.splitext(os.path.basename(__file__))[0], exc))

# 8x8 (Red, Green, Blue) LED matrix surface
LEDMatrix = [
    [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
    [0, 0, 0], [0, 0, 0],
    [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
    [0, 0, 0], [0, 0, 0],
    [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
    [0, 0, 0], [0, 0, 0],
    [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
    [0, 0, 0], [0, 0, 0],
    [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
    [0, 0, 0], [0, 0, 0],
    [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
    [0, 0, 0], [0, 0, 0],
    [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
    [0, 0, 0], [0, 0, 0],
    [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
    [0, 0, 0], [0, 0, 0]
]

# Explosion animation on the RGB color LED matrix
LEDExplosionPattern = [
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 2, 2, 2, 2, 1, 0],
                            [0, 1, 2, 3, 3, 2, 1, 0],
                            [0, 1, 2, 3, 3, 2, 1, 0],
                            [0, 1, 2, 2, 2, 2, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]
                    ]

# For shifting the animation sequence in 'LEDExplosionPattern'
__explosionShift = 0
# Represent the brightness of LED color which is used for fading effect
__explosionFade = 0
# Animation time of the explosion before fading
__explosionTimer = 0


def clear():
    if not sense:
        return

    for l in LEDMatrix:
        for i in range(3):
            l[i] = 0
    sense.set_pixels(LEDMatrix)


def randomFill():
    if not sense:
        return

    for l in LEDMatrix:
        # Fill up the 8x8 LED matrix surface with random RGB colors
        for i in range(3):
            l[i] = random.randint(0, 255)
    sense.set_pixels(LEDMatrix)


def plotLED(x, y, col):
    p = LEDMatrix[y * 8 + x]
    p[0], p[1], p[2] = (col[0], col[1], col[2])


def getPixel(x, y):
    return LEDMatrix[y * 8 + x]


def showOrientation(h, v):
    if not sense:
        return

    clear()
    # Calculate the postition to start drawing the light blue
    # block on LED matrix.
    startX = 4 + int(h * (3.0 if h > 0 else 4.0))
    startY = 4 + int(v * (3.0 if v > 0 else 4.0))

    # Draw blue box on LED matrix surface
    col = 255
    for x in range(startX, 8):
        for y in range(0, 8):
            p = getPixel(x, y)
            p[2] = col
        col -= 35

    if startX > 0:
        col = 225
        for x in range(startX - 1, -1, -1):
            for y in range(0, 8):
                p = getPixel(x, y)
                p[2] = col
            col -= 35

    col = 255
    for y in range(startY, 8):
        for x in range(0, 8):
            p = getPixel(x, y)
            # Fill the rest of LED matrix surface with red color
            p[0] = 255 - col
            if col > 128 and p[2] > 128:
                # Change the blue box to cyan color
                p[1] = col
            else:
                # Add some randomness to the rest of LED matrix surface
                for i in range(1, 3):
                    p[i] = random.randint(0, col)

        col -= 35

    if startY > 0:
        col = 225
        for y in range(startY - 1, -1, -1):
            for x in range(0, 8):
                p = getPixel(x, y)
                p[0] = 225 - col
                if col > 128 and p[2] > 128:
                    p[1] = col
                else:
                    for i in range(1, 3):
                        p[i] = random.randint(0, col)
            col -= 35

    sense.set_pixels(LEDMatrix)


# Call this function to re-initialize the explosion animation
def resetExplosion():
    global __explosionShift, __explosionFade, __explosionTimer

    clear()
    __explosionShift = 0
    __explosionFade = 64
    __explosionTimer = pygame.time.get_ticks() + 1600


# Keep calling this function repeatedly to animate the explosion on LED matrix
def showExplosion():
    global __explosionShift, __explosionFade, __explosionTimer

    if not sense or __explosionFade <= 0:
        return True

    for y in range(8):
        for x in range(8):
            c = ((LEDExplosionPattern[y])[x] + __explosionShift) % 4
            sense.set_pixel(x, y, (__explosionFade * 4) - 1,
                            (__explosionFade * (c + 1)) - 1, 0)

    # Shift the explosion animation frame
    __explosionShift += 1
    __explosionShift %= 4
    if pygame.time.get_ticks() > __explosionTimer:
        # Start fading the explosion animation
        __explosionFade -= 8

    if not __explosionFade:
        # Clear the matrix LED when the animation is completely faded
        clear()

    # Return TRUE when done animating the explosion
    return (__explosionFade <= 0)


if sense:
    sense.low_light = False
