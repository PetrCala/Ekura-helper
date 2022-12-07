import numpy as np
import random
from datetime import datetime, timedelta
import re
import time
import math
import sys

from ctypes import windll
import cv2
from PIL import ImageGrab
from cv2 import mean #Capturing screen
from pynput.keyboard import Key, HotKey, Controller
import pytesseract #Text recognition
import pywintypes
import win32.win32gui as win32gui

from scripts.base import Base
from tools import static
from tools import local_settings
from tools.directKeys import click, queryMousePosition, PressKey, ReleaseKey, moveMouseTo

windll.user32.SetProcessDPIAware() #Make windll properly aware of your hardware
pytesseract.pytesseract.tesseract_cmd = static.PYTESSERACT_PATH # Pytesseract path
keyboard = Controller()

class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()

class Launcher(Base):
    def __init__(self):
        pass

    def main(self):
        # self.openGameLauncher()
        pass

    @property
    def screen_pos(self):
        '''Position of the launcher. Kept as a property, in order to allow for opening
        of the launcher window after constructing the class.
        '''
        hwnd = self.getLauncherHwnd()
        return hwnd if hwnd is None else self.getLauncherCoords()

    def getLauncherHwnd(self):
        '''Get window handle number of the game launcher window.
        '''
        return self.getWindowHwnd(static.LAUNCHER_WINDOW_NAME)

    def getLauncherCoords(self):
        '''Get coordinates of the game launcher window.
        '''
        hwnd = self.getLauncherHwnd()
        return self.getWindowCoords(hwnd)

    def openGameLauncher(self):
        '''Open the game launcher.
        '''
        self.useKey(Key.cmd, sleep = 0.2)
        self.useKeys(static.LAUNCHER_APP_NAME, sleep_after=0.3) # Write the game launcher name
        self.useKey(Key.enter, sleep = 0.9)
        tries = 0 # Placeholder for the upper limit on the window opening wait time
        hwnd = self.getLauncherHwnd()
        while hwnd is None and tries < 20: # Requires manual input for the UAC
            time.sleep(0.5) # Wait for the window to open
            hwnd = self.getLauncherHwnd()
            tries += 1
        if hwnd is None:
            print('Could not open the launcher window')
            return False
        time.sleep(2) # Wait for the launcher animations to finish
        x_, y_ = static.LAUNCHER_DEFAULT_COORD[0], static.LAUNCHER_DEFAULT_COORD[1]
        # win32gui.MoveWindow(hwnd, x_, y_) # Move the window to the default coordinates
        print('Launcher open')
        return True

    def closeGameLauncher(self):
        '''Close the game launcher.
        '''
        hwnd = self.getLauncherHwnd()
        if hwnd is None: # Launcher not open
            return True 
        win32gui.CloseWindow(hwnd)
        return True

    def defaultNameEntered(self):
        '''Check whether there is not already a name input by default.
        If yes, return this name, if not, return False.
        '''
        pass

    def inputName(self):
        '''Input the character name into the game launcher. Assumer the launcher is
        already open.
        '''
        
        pass

    def inputPassword(self):
        '''Input the character password into the game launcher. Assumer the launcher is
        already open.
        '''
        pass

    def login(self):
        '''Input the name, password, and start the game. The game launcher window
        must be open already.
        '''
        if not self.checkLauncherOpen():
            self.openGameLauncher()
        self.inputName()
        self.inputPassword()
        self.useKey(Key.enter, sleep = False) # Press 'start game' (may be changed to click)
        return True

    def checkLauncherOpen(self):
        '''Check whether the game launcher is open or not. If yes,
        return True. If not, return False.
        '''
        hwnd = self.getLauncherHwnd()
        if hwnd is None:
            return False
        return True