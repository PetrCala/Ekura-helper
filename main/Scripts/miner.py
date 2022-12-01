from ctypes import windll
import cv2
from PIL import ImageGrab
from cv2 import mean #Capturing screen

from base import Base
from static import *
from pynput.keyboard import Key, HotKey, Controller
import pytesseract #Text recognition
from directKeys import click, queryMousePosition, PressKey, ReleaseKey, moveMouseTo, SPACE

import numpy as np
import time
import math
import sys

windll.user32.SetProcessDPIAware() #Make windll properly aware of your hardware
pytesseract.pytesseract.tesseract_cmd = PYTESSERACT_PATH # Pytesseract path
keyboard = Controller()

class Miner(Base):
    def __init__(self):
        pass
        self.mining_finished = True # Boolean to indicate finished mining

    def main(self):
        '''Main method of the Miner class
        '''
        #self.clickScreen()
        #self.useKey('W', method = 'press')
        #time.sleep(2)
        #self.useKey('W', method = 'release')

        #Main method
        # self.mine()
        # self.printMousePosition()

        #Various method
        #self.openScreen()

        return None

    def initiate_mining(self, node:list):
        '''Insert a pair of coordinates as a list and start mining at these coordinates.
        '''
        moveMouseTo(node[0], node[1]) #Target the node
        time.sleep(0.5) # Allow for cursor positioning
        click(node[0], node[1]) #Click the node
        self.mining_finished = False # Mining started
        return None

    def check_mining_status(self):
        '''Check whether the mining has yet finished. If so, set the '.mining_finished'
        attribute to True. Return None.
        '''
        if 1 == 1: # Mining is done - finish this part
            self.mining_finished = True
        return None

    def mine(self):
        '''Find the node on the screen and click it. After mining is done, collect the fallen ore.
        '''
        print('Initiating mining...')
        match_list = self.pixelsOnScreen(NODE_PIXELS) #Searching for node name
        node = self.calculateNodePosition(match_list) #Approximating the node position
        if node is None: #Node not found on the screen
            print(f'Failed to find a node.')
            return None
        #Mine
        self.initiate_mining(node)
        if self.mining_finished: # Mining initialization failed
            print('Failed to initiate mining')
            return None
        while self.mining_finished is False: # Wait until mining is finished
            time.sleep(3) # Wait a while - maybe randomize this
            self.check_mining_status() # If mining is over, set '.mining_finished' to false
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


if __name__ == '__main__':
    M = Miner()
    M.main()
    

#Useful
#(58, 144, 76) <- surely part of the node, 18 matches - green name
#(146, 126, 134) <- diamond ore, possibly
