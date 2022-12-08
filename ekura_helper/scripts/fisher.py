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
from scripts.base import InGameBot
from tools import static
from tools import local_settings
from tools.directKeys import click, queryMousePosition, PressKey, ReleaseKey, moveMouseTo

windll.user32.SetProcessDPIAware() #Make windll properly aware of your hardware
pytesseract.pytesseract.tesseract_cmd = static.PYTESSERACT_PATH # Pytesseract path
keyboard = Controller()

class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()

class Fisher(InGameBot):
    '''A class for automatic fishing. Assumes you have the fishing rod equipped.

    Args:
        InGameBot (_type_): _description_
    '''
    def __init__(self, char_name:str, *args, **kwargs):
        '''Constructor for the Fisher class. Game must be running in order for the
            constructor to be callable.

        Args:
            char_name (str): Name of the character which shall be operated by the bot.
        '''
        # Attributes
        self.fishing_timer = datetime.now() + timedelta(days = -1)
        # Constructor operations
        super(Fisher, self).__init__(char_name, *args, **kwargs) # Master class inheritance

    def main(self):
        '''Main method of the Miner clsass
        '''
        pass


    def prepareForFishing(self):
        '''Check all the necessary requirements to start fishing.
        '''
        self.focusedInput('SPACE')
        time.sleep(1)
        msg = self.readTextInRange(static.MESSAGE_LOG_COORD, view_range=False)
        print(msg)
        pass

    def fish(self):
        '''Assuming all fishing requirements were fulfilled, put on a bait
        and start fishing. Return True if the fishing was successful, and
        False otherwise.
        '''
        pass



    
