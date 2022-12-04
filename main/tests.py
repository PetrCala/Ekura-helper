from ctypes import windll
import cv2
from PIL import ImageGrab
from cv2 import mean #Capturing screen
from pynput.keyboard import Key, HotKey, Controller
import pytesseract #Text recognition
import pywintypes
import win32.win32gui as win32gui

from Scripts.base import Base
from Scripts.static import *
from Scripts.miner import Miner
from Scripts.directKeys import click, queryMousePosition, PressKey, ReleaseKey, moveMouseTo

import numpy as np
import random
from datetime import datetime, timedelta
import re
import time
import math
import sys

from Scripts.static import *
# from local_settings import *

windll.user32.SetProcessDPIAware() #Make windll properly aware of your hardware
pytesseract.pytesseract.tesseract_cmd = PYTESSERACT_PATH # Pytesseract path
keyboard = Controller()


def main():
    M = Miner(char_name = MINER_CHAR_NAME)
    M.main()



if __name__ == '__main__':
    main()