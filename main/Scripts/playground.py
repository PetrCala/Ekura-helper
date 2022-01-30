from ctypes import windll
import cv2
from PIL import ImageGrab
import numpy as np
from directKeys import click, queryMousePosition, PressKey, ReleaseKey, moveMouseTo, SPACE
import time
import math
import sys


#windll = c.windll.kernel32
#cdll = c.cdll.msvcrt
#test = c.c_int()

class Miner():
    def __init__(self):
        self.screen_size = self.getScreenSize()
        self.screen_pos = self.getScreenCoordinates(self.screen_size) #Position/coordinates of the screen
        #self.game_coords = self.getGameCoords(self.screen_pos)


    def getGameCoords(self):
        '''
        Return a list of 4 coordinates marking the active game window.

        Check for ... and ..., from which the game window size and position is computed.
        '''
        pos = self.screen_pos
        screen = self.createScreen(pos) #Computer screen

        print(screen)
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        
        return [x1,y1,x2,y2]


    #Delete later
    def mouseIn(self):
        on_screen = self.mouseOnScreen(self.screen_pos)
        state = 'is' if on_screen else 'is not'
        print(f'The mouse {state} on screen.')
    
    @staticmethod
    def mouseOnScreen(screen_pos):
        '''Specify the screen position as a list of coordinates and check whether the mouse is within these coordinates.

        Args:
            screen_pos ([type]): [description]

        Returns:
            bool: True if the mouse is within the specified coordinates, False otherwise.
        '''
        assert isinstance(screen_pos, list) and len(screen_pos) == 4, 'The screen element is misspecified'
        pos = queryMousePosition() #Get mouse position
        on_screen = screen_pos[0] < pos.x < screen_pos[2] and screen_pos[1] < pos.y < screen_pos[3]
        return True if on_screen else False

    @staticmethod
    def createScreen(screen_pos):
        screen = np.array(ImageGrab.grab(bbox=screen_pos))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        return screen

    @staticmethod
    def getScreenCoordinates(screen_size):
        '''Return a list of 4 coordinates marking the beginning and end of the screen.

        Args:
            screen_size ([list]): A 2 elements long list denoting the screen size.

        Returns:
            list: A list of coordinates in the form [x1,y1, x2, y2].
        '''
        screen_pos = [0,0] + screen_size
        return screen_pos

    @staticmethod
    def getScreenSize():
        '''
        A class method for retrieving the screen resolution.

        Returns:
            list: A list of two coordinates marking the bottom right part of the screen.
        '''
        if sys.platform[0:3] == 'win':
            user32 = windll.user32

            return [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        else:
            raise SystemError('The code must be ran on the Windows platform')

    @staticmethod
    def dist(x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


if __name__ == '__main__':
    M = Miner()
    #M.mouseIn()
    M.getGameCoords()

#printMousePosition()