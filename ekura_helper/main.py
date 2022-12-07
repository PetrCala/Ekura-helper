import os
import sys

from ctypes import windll
from pynput.keyboard import Key, HotKey, Controller
import pytesseract #Text recognition
import win32.win32gui as win32gui

from scripts.base import Base
from scripts.launcher import Launcher
from scripts.miner import Miner
from scripts.screenalysis import Screenalysis
from tools import static
from tools import local_settings
from tools.directKeys import click, queryMousePosition, PressKey, ReleaseKey, moveMouseTo

windll.user32.SetProcessDPIAware() #Make windll properly aware of your hardware
pytesseract.pytesseract.tesseract_cmd = static.PYTESSERACT_PATH # Pytesseract path
keyboard = Controller()

def main():
     M = Miner(char_name = local_settings.MINER_CHAR_NAME)
     M.main()
    # #L = Launcher()
    # #L.main()

if __name__ == '__main__':
    main()
