from ctypes import windll
import cv2
from PIL import ImageGrab
from cv2 import mean #Capturing screen
from pynput.keyboard import Key, HotKey, Controller
import pytesseract #Text recognition

from Scripts.base import Base
from Scripts.static import *
from Scripts.miner import Miner
from Scripts.directKeys import click, queryMousePosition, PressKey, ReleaseKey, moveMouseTo

import numpy as np
import re
import time
import math
import sys

windll.user32.SetProcessDPIAware() #Make windll properly aware of your hardware
pytesseract.pytesseract.tesseract_cmd = PYTESSERACT_PATH # Pytesseract path
keyboard = Controller()


def main():
    M = Miner()

    print('hello')





if __name__ == '__main__':
    M = Miner()


