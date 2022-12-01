from ctypes import windll
import cv2
from PIL import ImageGrab
from cv2 import mean #Capturing screen

from base import Base
from static import *
from pynput.keyboard import Key, HotKey, Controller
from pynput import mouse
import pytesseract #Text recognition
from directKeys import click, queryMousePosition, PressKey, ReleaseKey, moveMouseTo

import numpy as np
import time
import math
import sys

windll.user32.SetProcessDPIAware() #Make windll properly aware of your hardware
pytesseract.pytesseract.tesseract_cmd = PYTESSERACT_PATH # Pytesseract path
keyboard = Controller()

class Screenalysis(Base):
    def __init__(self):
        pass

    def main(self):
        # pixel = self.getPixelRGB()
        # print(pixel)
        self.getPixelRGB()
        #self.getMousePosition(scale = True, verb = True)        

    def calculateCoordRange(self):
        '''Click twice on the screen, and return a list of coordinates marking
        both these points.

        Note:
            -The first specified coordinate should be top left of the screen,
                and the second should be the bottom right.
        '''
        print('Please click on the top left corner of the desired range:')
        pass


    def getPixelRGB(self):
        '''Get a RGB value of the pixel the mouse is pointing at.

        Returns:
            list: RGB value returned as a list in the order R,G,B.
        '''
        assert self.mouseOnScreen(self.screen_pos), 'The mouse is not on screen'
        mouse = queryMousePosition() #Get mouse position
        x, y = mouse.x, mouse.y
        screen = self.createScreen(color_scale = 'orig') #Computer screen snapshot
        (r, g, b) = screen[y,x]
        print(f"Pixel at ({x}, {y}) - Red: {r}, Green: {g}, Blue: {b}")
        return [r,g,b]


if __name__ == '__main__':
    S = Screenalysis()
    S.main()
    
