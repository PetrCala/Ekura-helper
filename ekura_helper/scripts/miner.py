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
from tools.directkeys import click, queryMousePosition, PressKey, ReleaseKey, moveMouseTo

windll.user32.SetProcessDPIAware() #Make windll properly aware of your hardware
pytesseract.pytesseract.tesseract_cmd = static.PYTESSERACT_PATH # Pytesseract path
keyboard = Controller()


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()

class Miner(InGameBot):
    def __init__(self, char_name:str, *args, **kwargs):
        '''Constructor for the Miner class. Game must be running in order for the
            constructor to be callable.

        Args:
            char_name (str): Name of the character which shall be operated by the bot.
        '''
        # Attributes
        self.mining_finished = True # Boolean to indicate finished mining
        self.mining_impossible = True # There is no ore to mine - search/wait for a new one
        self.mining_timer = datetime.now() + timedelta(days = -1)
        # Constructor operations
        super(Miner, self).__init__(char_name, *args, **kwargs) # Master class inheritance

    def main(self):
        '''Main method of the Miner clsass
        '''
        while True:
            mining_successful = self.mineOre()
            if not mining_successful: # Ore was not found
                time.sleep(7)

    def mineOre(self):
        '''Initiate the mining process, and keep mining until there is no ore to mine.
        Return True, if mining was successful, and False, if not.
        '''
        times_mined = 0
        # Search for the node
        print('Looking for a node to start mining...')
        node = self.findNode()
        if node is None:
            return False # No node on the screen to mine (automatically throws a message)
        # Start the mining process
        print('Found a node. Starting the mining process...')
        self.mining_impossible = False # Found a node
        while self.mining_impossible is False and times_mined < 35:
            self.mineOnce(node) # Mine
            node_unmoved = self.checkNode(node) # Fast check
            if not node_unmoved: # Node/camera position was changed
                node = self.findNode() # Screen-wide check
                if node is None:
                    self.mining_impossible = True
                    break
            times_mined += 1
        print('Mining is over. There is no more ore to be mined.')
        return True

    def checkMiningFinished(self):
        '''Check whether the mining has yet finished. If so, set the 'mining_finished'
        attribute to True. Return True, if mining is finished, and False otherwise.
        '''
        msg = self.readTextInRange(static.MESSAGE_LOG_COORD, view_range = False) # Read message log
        ore_gone = self.checkStringForMatches(msg, static.MINING_IMPOSSIBLE_KEYWORDS, verbose = False)
        matches = self.checkStringForMatches(msg, static.MINING_DONE_KEYWORDS, verbose = False)
        if ore_gone > 1: # Check whether the node had not disappeared yet
            print('The node has disappeared...')
            self.mining_impossible = True
            self.mining_finished = True
            return True
        if matches > 1:
            if (datetime.now() - self.mining_timer) < timedelta(seconds=8): # Last message had not yet disappeared
                print('Waiting for the message to disappear...')
                return False
            self.mining_finished = True
        if ore_gone > 1 or matches > 1:
            self.mining_timer = datetime.now() # Update mining timer
            return True
        return False

    def findNode(self):
        '''Return a list of coordinates, if node is present on the screen. Return False otherwise.
        '''
        match_list = self.pixelsOnScreen(static.NODE_PIXELS) #Searching for node name
        node = self.calculateNodePosition(match_list) #Approximating the node position
        if node is None: #Node not found on the screen
            print('Failed to find an node.')
            return None
        return node # [x,y]

    def checkNode(self, presumed_pos:list):
        '''Input a list of coordinates, where the node is presumed to be located.
        Perform a narrow check for said node, and return True, if the node is still
        at the same location. Return False otherwise.

        Args:
            presumed_pos (list): List of coordinates. 
        '''
        y_offset = 100 # Node located approximately this many pixels below text
        x_width = 50 # Search area pixels - x axis 
        y_width = 30 # Search area pixels - y axis 
        # Specify the check range
        x_, y_ = presumed_pos[0], presumed_pos[1] - y_offset
        range_coords = [int(x_ - x_width/2), int(y_ - y_width/2), int(x_ + x_width/2), int(y_ + y_width/2)]
        # Check said range
        match_list = self.pixelsOnScreen(static.NODE_PIXELS, range_coords) # Node position check
        matched_pixels = len(match_list)
        # Decide whether or not the node is present
        if matched_pixels > 10: # Arbitrary number
            print('The node is still there. Mine away.')
            return True
        print('The node could not be found, you should conduct a wider search.')
        return False

    def mineOnce(self, node:list):
        '''Find the node on the screen and click it. After mining is done, collect the fallen ore.
        '''
        times_checked = 0
        # Mine
        print('Initiating mining...')
        x_, y_ = self.randomizeClicking(node[0], node[1]) # Move the cursor slightly
        self.focusedClick(x_, y_) # Click the node
        self.mining_finished = False # Mining started
        while self.mining_finished is False and times_checked < 22: # Wait until mining is finished
            time.sleep(2) # Wait a while
            self.checkMiningFinished() # Is mining finished (or over)
            times_checked += 1
        # Collect ore
        self.focusedInput('Z') # Collect fallen ore
        print(f'Mining complete.')
        return None

    @staticmethod
    def calculateNodePosition(match_list):
        '''Input a list of coordinates where a match was found with the node name on the screen
        and determine the approximate node position.

        Args:
            match_list (list): A (nested) list of coordinates

        Returns:
            list: The coordinates where the node should be located on the screen.

        The method assumes the camera is maximally zoomed out, at an angle parallel to the ground
        '''
        if match_list == []:
            print('The node location could not be calculated. There are no matching pixels on the screen.')
            return None
        y_offset = 100 # Rough estimate of how many pixels below the text the node is located
        x, y = [item[0] for item in match_list], [item[1] for item in match_list]
        x_, y_ = int(sum(x)/len(x)), int(sum(y)/len(y)) # Mean value for both coordinates
        node = [x_, y_ + y_offset] # Offest Y

        print(f'The node should be located at these coordinates: x={node[0]}, y={node[1]}.')
        #Here try to integrate the existing camera position, proximity to the node etc
        return node # [x, y]