![Alt text](res/img/title.png?raw=true "SPYShip")  
SPYShip is an open source classic retro arcade space shooter game written in Python 3.

## System Requirements
Python 3.5.3 or later  
Pygame 1.9.3 or later

Sense HAT support is optional.  
For more details on Sense HAT visit:  
https://www.raspberrypi.org/products/sense-hat/

NOTE: "Sense HAT" python module is needed to support Sense HAT.

## Getting Started
1) Use git or the download button to download the game source code.
2) Change to the game root directory.
3) Start the game as follow:
```
python main.py
```

To use Sense HAT as game input controller on Raspberry Pi 3, change the following line in [gameconfig.py](gameconfig.py):
```
INPUT_CONTROLLER = INPUT_SENSEHAT
```

## How To Play
Keyboard as game input controller:

Move Up      - 'W' or UP arrow key  
Move DOwn    - 'S' or DOWN arrow key  
Move Left    - 'A' or LEFT arrow key  
Move Right   - 'D' or RIGHT Arrow key  
Select/Shoot - SPACEBAR or ENTER  

Sense HAT as game input controller:

Tilt the Sense HAT to move the spaceship up, down, left or right.  
Press the five-button joystick to select/shoot.  
Push the five-button joystick up or down to change selection in main menu.

NOTE: Just press the 'shoot' button once to start shooting. Press the same button again to stop shooting.

## Documentation
Check out this project's [wiki](https://github.com/JeremyAngCH/spyship/wiki) pages.

## Game Play Video
https://www.youtube.com/watch?v=vu90Qnr1ayE

## Credits
See the [CREDITS.md](CREDITS.md) file for details.

## License
Source codes and game images are available under the MIT license. You are encouraged to publish/distribute this game with or without modification to source code but with alternative game images.
