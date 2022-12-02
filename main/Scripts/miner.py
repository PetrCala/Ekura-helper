from ctypes import windll
import cv2
from PIL import ImageGrab
from cv2 import mean #Capturing screen
from pynput.keyboard import Key, HotKey, Controller
import pytesseract #Text recognition

from .base import Base
from .static import *
from .directKeys import click, queryMousePosition, PressKey, ReleaseKey, moveMouseTo

import numpy as np
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

class Miner(Base):
    def __init__(self):
        self.mining_finished = True # Boolean to indicate finished mining
        self.mining_impossible = True # There is no ore to mine - search/wait for a new one

    def main(self):
        '''Main method of the Miner clsass
        '''
        self.mineOre()
        return None

    def mineOre(self):
        '''Initiate the mining process, and keep mining until there is no ore to mine.
        '''
        current_char_pos = self.char_pos
        print(current_char_pos)
        times_mined = 0
        print('Looking for a node to start mining...')
        node = self.findNode()
        if node is None:
            return None # No node on the screen to mine (automatically throws a message)
        print('Found a node. Starting the mining process...')
        self.mining_impossible = False # Found a node
        while self.mining_impossible is False and times_mined < 35:
            self.mineOnce(node)
            if current_char_pos != self.char_pos: # Re-check character position
                node = self.findNode()
                if node is None:
                    self.mining_impossible = True
                    break
            times_mined += 1
        print('Mining is over. There is no more ore to be mined.')
        return None

    def initiateMining(self, node:list):
        '''Insert a pair of coordinates as a list and start mining at these coordinates.
        '''
        moveMouseTo(node[0], node[1]) #Target the node
        time.sleep(0.5) # Allow for cursor positioning
        click(node[0], node[1]) #Click the node
        self.mining_finished = False # Mining started
        return None

    def updateMiningStatus(self):
        '''Check whether the mining has yet finished. If so, set the 'mining_finished'
        attribute to True. Return None.
        '''
        msg = self.readTextInRange(MINING_TEXT_COORD, view_range = False) # Read message log
        matches = self.checkStringForMatches(msg, MINING_DONE_KEYWORDS, verbose = False)
        if matches > 1:
            self.mining_finished = True
        ore_gone = self.checkStringForMatches(msg, MINING_IMPOSSIBLE_KEYWORDS, verbose = False)
        if ore_gone > 1: # Check whether the node had not disappeared yet
            self.mining_impossible = True
        return None

    def findNode(self):
        '''Return a list of coordinates, if node is present on the screen. Return False otherwise.
        '''
        match_list = self.pixelsOnScreen(NODE_PIXELS) #Searching for node name
        node = self.calculateNodePosition(match_list) #Approximating the node position
        if node is None: #Node not found on the screen
            print('Failed to find an node.')
            return None
        return node

    def mineOnce(self, node:list):
        '''Find the node on the screen and click it. After mining is done, collect the fallen ore.
        '''
        times_checked = 0
        print('Initiating mining...')
        self.initiateMining(node)
        if self.mining_finished: # Mining initialization failed
            print('Failed to initiate mining')
            return None
        while self.mining_finished is False and times_checked < 30: # Wait until mining is finished
            time.sleep(2) # Wait a while - maybe randomize this
            self.updateMiningStatus() # If mining is over, set the 'mining_finished' attribute to false
            times_checked += 1
        self.useKey('Z') # Collect fallen ore
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
        x, y = [item[0] for item in match_list], [item[1] for item in match_list]
        x_, y_ = int(sum(x)/len(x)), int(sum(y)/len(y)) # Mean value for both coordinates
        node = [x_, y_ + 100] #The node should be roughly 220 pixels below the node name

        print(f'The node should be located at these coordinates: x={node[0]}, y={node[1]}.')
        #Here try to integrate the existing camffera position, proximity to the node etc
        return node

    @property
    def char_pos(self):
        '''Position of the character, given by two coordinates.
        '''
        raw_coords = self.readTextInRange(CHAR_POS_COORD)
        if not re.match(CHAR_POS_REGEX, raw_coords):
            raise ValueError('Could not identify the character\'s coordinates.')
        coords_set = re.match(CHAR_POS_REGEX_EXTRACT, raw_coords)
        coords = [int(coords_set[1]), int(coords_set[2])] # [x,y]
        return coords

if __name__ == '__main__':
    M = Miner()
    M.main()
    

#Useful
#(58, 144, 76) <- surely part of the node, 18 matches - green name
#(146, 126, 134) <- diamond ore, possibly
