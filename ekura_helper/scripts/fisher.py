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
        self.fishing_impossible = True
        self.fishing_finished = True
        self.check_interval = 1 # Float, amount of time to wait before checking fishing state
        self.fishing_timer = datetime.now() + timedelta(days = -1)
        # Constructor operations
        super(Fisher, self).__init__(char_name, *args, **kwargs) # Master class inheritance

    def main(self):
        '''Main method of the Miner clsass
        '''
        while True:
            fishing_count = 0
            self.fishing_impossible = False # Allow for fishing to start
            while (not self.fishing_impossible) and (fishing_count <= 10):
                self.fish()
                fishing_count += 1

    def fish(self):
        '''Assuming all fishing requirements were fulfilled, start fishing.
        Return True if the fishing was successful, and False otherwise.
        '''
        time_checked = 0
        start = time.time()
        self.focusedInput('SPACE')
        time.sleep(0.4) # Wait for the message to appear
        we_fishing = self.checkIfFishingStarted()
        if we_fishing is False: # Start fishing (check automatically puts on lure)
            time.sleep(0.2) # Allow for proper refocusing
            self.focusedInput('SPACE')
        self.fishing_finished = False # Fishing started
        print('Initiating fishing...')
        time.sleep(3) # Wait for the messages to disappear
        while (not self.fishing_finished) and (time_checked < 50):
            fishing_state = self.checkFishingState()
            if isinstance(fishing_state, str): # Fish caught
                print(f'{fishing_state} found. The wait took {round(time.time() - start, 2)} seconds.')
                wait_time = self.calculateFishWaitTime(fishing_state)
                randomized_wait_time = self.randomizeWaitTime(wait_time) # Against bot detection
                time.sleep(randomized_wait_time)
                print(f'Pulling up after {round(randomized_wait_time, 2)} seconds...')
                self.focusedInput('SPACE') # Pull up
                time.sleep(4) # Wait for the animations to finish
                self.fishing_finished = True
                print('Fish pulling complete.')
                return True
            time.sleep(self.check_interval) # Wait before checking again
            time_checked += 1
        print('Could not find any fish. Trying again...')
        return True

    def checkIfFishingStarted(self):
        '''Check all the necessary requirements to start fishing. If all are fulfilled,
        return True, else return False.
        '''
        msg = self.readTextInRange(static.MESSAGE_LOG_COORD, view_range=False)
        fishing_impossible = self.checkStringForMatches(msg, static.FISHING_IMPOSSIBLE_KEYWORDS, verbose = False)
        if fishing_impossible > 0:
            print('You can not fish here...')
            self.fishing_impossible = True
            return False
        no_lure = self.checkStringForMatches(msg, static.FISHING_NO_LURE_KEYWORDS, verbose = False)
        if no_lure > 1:
            time.sleep(0.2) # Allow for proper input
            print('No bait is on. Putting on bait...')
            self.focusedInput(static.FISHING_LURE_SLOT) # Put on lure
            return False
        self.fishing_impossible = False
        return True

    def checkFishingState(self):
        '''A method for periodically checking whether the fishing has finished yet.
        If a fish has been spotted, return a string with the name of the fish,
        otherwise return None.
        '''
        # If not fishing, set self.fishing_finished to False
        msg = self.readTextInRange(static.MESSAGE_LOG_COORD, view_range=False)
        msg_parts = msg.split()
        if ('že' in msg_parts) and ('právě' in msg_parts):
            fish_type = self.readFishType(msg)
            return fish_type
        fishing_failed = self.checkStringForMatches(msg, static.FISHING_FISH_GONE_KEYWORDS)
        if fishing_failed > 1:
            print('Failed to catch the fish.')
            self.fishing_finished = True
            time.sleep(4) # Waiting for the fishing state to reset
        return None
        
    def randomizeWaitTime(self, time:float):
        '''Input a float indicating fish wait time, and randomize it
        by shifting it several tenths of a second in either direction.
        Return the new time.
        :args:
            time (float): Time to wait.
        '''
        bias = self.check_interval / 2 # Expected bias induced by imprecise checking
        lower_bound = (-1) - bias
        upper_bound = 1 - bias
        offset = random.uniform(lower_bound, upper_bound) 
        return time + offset

    @staticmethod
    def readFishType(msg:str):
        '''Input the message with the fish on the rod, return an integer
        indicating the seconds necessary.
        '''
        # Possibly change into regex later
        fish_list = []
        msg_parts = msg.split()
        idx_before = msg_parts.index('že') + 1
        idx_after = msg_parts.index('právě')
        for i in range(idx_before, idx_after):
            fish_list.append(msg_parts[i])
        fish_type = ' '.join(fish_list)
        return fish_type

    @staticmethod
    def calculateFishWaitTime(fish_name:str):
        '''Input a fish name and return its wait time.
        '''
        res = next((sub for sub in static.FISHING_FISH_INFORMATION if fish_name in sub['Fish names']), None)
        if res is None:
            print(f'{fish_name} is not in our library... Let\'s wait randomly until pulling up')
            return 5
        return res['Time']

        