from ctypes import windll
import cv2
from PIL import ImageGrab
from cv2 import mean #Capturing screen
from pynput.keyboard import Key, HotKey, Controller
import pytesseract #Text recognition
import pywintypes
import win32.win32gui as win32gui

from base import Base
from static import *
# from main.local_settings import *
from directKeys import click, queryMousePosition, PressKey, ReleaseKey, moveMouseTo

import numpy as np
import random
from datetime import datetime, timedelta
import re
import time
import math
import sys

windll.user32.SetProcessDPIAware() #Make windll properly aware of your hardware
pytesseract.pytesseract.tesseract_cmd = PYTESSERACT_PATH # Pytesseract path
keyboard = Controller()

class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()

class Launcher(Base):
    def __init__(self):
        pass

    def main(self):
        coords = self.getLauncherCoords()
        mouse_pos = self.getMousePosition()
        launcher_coords = self.calculateCoords(mouse_pos, from_scale = False)
        print(launcher_coords) # Get launcher window coordinates
        pass

    @property
    def screen_pos(self):
        '''Change operation window to the game launcher window.
        '''
        return self.getLauncherCoords()

    def getLauncherHwnd(self):
        '''Get window handle number of the game launcher window.
        '''
        return self.getWindowHwnd(LAUNCHER_WINDOW_NAME)

    def getLauncherCoords(self):
        '''Get coordinates of the game launcher window.
        '''
        hwnd = self.getLauncherHwnd()
        return self.getWindowCoords(hwnd)

    def openGameLauncher(self):
        '''Open the game launcher, if not open already.
        '''
        # Finish this
        return True

    def closeGameLauncher(self):
        '''Close the game launcher.
        '''
        hwnd = self.getLauncherHwnd()
        if hwnd is None: # Launcher not open
            return True 
        win32gui.CloseWindow(hwnd)
        return True

    def login(self):
        '''Input the name, password, and start the game. The game launcher window
        must be open already.
        '''
        if not self.checkLauncherOpen():
            self.openGameLauncher()
        # Finish this
        return True

    def checkLauncherOpen(self):
        '''Check whether the game launcher is open or not. If yes,
        return True. If not, return False.
        '''
        hwnd = self.getLauncherHwnd()
        if hwnd is None:
            return False
        return True
        

if __name__ == '__main__':
    L = Launcher()
    L.main()