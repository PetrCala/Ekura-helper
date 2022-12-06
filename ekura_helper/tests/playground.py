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

from ekura_helper.scripts.base import Base
from ekura_helper.tools import static
from ekura_helper.tools import local_settings
from ekura_helper.tools.directKeys import click, queryMousePosition, PressKey, ReleaseKey, moveMouseTo

windll.user32.SetProcessDPIAware() #Make windll properly aware of your hardware
pytesseract.pytesseract.tesseract_cmd = static.PYTESSERACT_PATH # Pytesseract path
keyboard = Controller()

#from Scripts.base import Base

def main():
    # M = Miner(char_name = MINER_CHAR_NAME)
    # M.main()
    print(static.NODE_PIXELS)
    # read = M.readTextInRange(MINING_TEXT_COORD)
    # print(read)



if __name__ == '__main__':
    main()