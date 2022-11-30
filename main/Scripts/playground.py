from ctypes import windll
import cv2
from PIL import ImageGrab
from cv2 import mean #Capturing screen
#import pytesseract #Text recognition
import numpy as np
from pynput.keyboard import Key, HotKey, Controller
import pytesseract #Text recognition
from directKeys import click, queryMousePosition, PressKey, ReleaseKey, moveMouseTo, SPACE
import time
import math
import sys

windll.user32.SetProcessDPIAware() #Make windll properly aware of your hardware
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract' # Pytesseract path
keyboard = Controller()

class Miner():
    def __init__(self):
        self.node_rgb = [[89, 220, 116], [70, 173, 91], [72, 180, 95], [91, 225, 119]] #RGB of pixels in the node name
        self.screen_size = self.getScreenSize()
        self.screen_pos = self.getScreenCoordinates(self.screen_size) #Position/coordinates of the screen
        self.mining_finished = True # Boolean to indicate finished mining

    def main(self):
        '''Main method of the Base class
        '''
        #self.clickScreen()
        #self.useKey('W', method = 'press')
        #time.sleep(2)
        #self.useKey('W', method = 'release')

        #Main method
        self.mine()
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
        match_list = self.pixelsOnScreen(self.node_rgb) #Searching for node name
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
    
    @property
    def numbers(self):
        '''A list of the 10 roman numbers as strings. Used for keyboard input.
        '''
        return [str(i) for i in range(11)]

    def createScreen(self, screen_pos = None):
        screen_pos = self.screen_pos if screen_pos is None else screen_pos #Defaults to the whole screen
        screen = np.array(ImageGrab.grab(bbox=screen_pos))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB) #Original color scale
        #screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY) #Grey color scale
        return screen

    def openScreen(self):
        '''Open the screenshot for viewing.
        '''
        win_name = 'Ekura screenshot'
        window_res = [int(self.screen_size[0]*0.9), int(self.screen_size[1]*0.9)]

        screen = self.createScreen() #Take a screenshot
        
        cv2.namedWindow(win_name, cv2.WINDOW_NORMAL) # Create a Named Window
        cv2.moveWindow(win_name, 0, 0) # Move it to (X,Y)
        cv2.imshow(win_name, screen) # Show the Image in the Window
        cv2.resizeWindow(win_name, window_res[0], window_res[1])   # Resize the Window
        cv2.waitKey(0); cv2.destroyAllWindows(); cv2.waitKey(1) #Handle closing of the window
        return None

    def getPixelRGB(self):
        '''Get a RGB value of the pixel the mouse is pointing at.

        Returns:
            list: RGB value returned as a list in the order R,G,B.
        '''
        assert self.mouseOnScreen(self.screen_pos), 'The mouse is not on screen'
        mouse = queryMousePosition() #Get mouse position
        x, y = mouse.x, mouse.y
        screen = self.createScreen() #Computer screen snapshot
        (r, g, b) = screen[y,x]
        print(f"Pixel at ({x}, {y}) - Red: {r}, Green: {g}, Blue: {b}")
        return [r,g,b]

    def pixelsOnScreen(self, rgb):
        '''
        Enter the r,g,b value of desirable pixel values and return a list with coordinates
            where these match on the screen.

        Arg:
            rgb [list] - This must be a nested list of possible rgb combinations, which should be
                searched.

        Returns:
            [list]: A list of the coordinates where the match was found
        '''
        assert any(isinstance(i, list) for i in rgb), 'The argument must be a nested list'
        print(f'Searching for pixel with rgb value {rgb}...')
        screen = self.createScreen() #Take a snapshot of the screen
        match_count = 0
        match_list = []
        start_time = time.time()
        for y in range(self.screen_size[1]):
            for x in range(self.screen_size[0]):
                pixel_rgb = screen[y,x].tolist()
                if pixel_rgb in rgb:
                    match_count = match_count + 1
                    print(f'Found a match at position ({x}, {y})')
                    match_list.append([x,y])
        search_time = round(time.time() - start_time, 2)
        print(f'Search complete.\nFound {match_count} matching pixels.\nThe search took {search_time} seconds.')
        return match_list

    def getMousePosition(self):
        m = queryMousePosition()
        x = m.x
        y = m.y
        print(f'The mouse position is\nx:{x}\ny:{y}')
        return None
    
    def num_key(self, key):
        '''Convert the string corresponding to a roman number to a key code legible by the keyboard.
        '''
        if not key in self.numbers:
            raise ValueError('Only roman numbers can be converted.')
        return keyboard._KeyCode(char = key)
        
    def useKeys(self, keys, sleep = True):
        '''For each key in keys, press this key. Keys can be any iterable object.
        '''
        for key in keys:
            self.useKey(key, sleep = sleep)
        return None

    def useKey(self, key, method = 'tap', sleep = True):
        '''An extended method for handling more complex key pressing.
        :args:
            key - Key to be pressed. Accepts all inputs of pynput, along with roman numbers in a string form (i.e. '5').
            method[str] - Method by which the key shall be used. Must be an attribute of the keyboard.
            sleep[bool] - If true, insert a 0.2 sleep time after the key press. Defaults to True.
        '''
        if not hasattr(keyboard, method):
            raise ValueError('You are trying to perform an invalid operation on the keyboard.')
        if key in self.numbers:
            key = self.num_key(key) #Parse a roman number
        getattr(keyboard, method)(key) #Tap, press,... the key
        if sleep:
            time.sleep(0.7)
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

    @staticmethod
    def mouseOnScreen(screen_pos):
        '''Specify the screen position as a list of coordinates and check whether the mouse is within these coordinates.

        Args:
            screen_pos ([type]): [description]

        Returns:
            bool: True if the mouse is within the specified coordinates, False otherwise.
        '''
        assert isinstance(screen_pos, list) and len(screen_pos) == 4, 'The screen element is misspecified'
        pos = queryMousePosition() #Get mouse position
        on_screen = screen_pos[0] < pos.x < screen_pos[2] and screen_pos[1] < pos.y < screen_pos[3]
        return True if on_screen else False

    @staticmethod
    def getScreenCoordinates(screen_size):
        '''Return a list of 4 coordinates marking the beginning and end of the screen.

        Args:
            screen_size ([list]): A 2 elements long list denoting the screen size.

        Returns:
            list: A list of coordinates in the form [x1,y1, x2, y2].
        '''
        screen_pos = [0,0] + screen_size
        return screen_pos

    @staticmethod
    def getScreenSize():
        '''
        A class method for retrieving the screen resolution.

        Returns:
            list: A list of two coordinates marking the bottom right part of the screen.
        '''
        if sys.platform[0:3] == 'win':
            user32 = windll.user32
            return [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        else:
            raise SystemError('The code must be ran on the Windows platform')

    @staticmethod
    def clickScreen():
        '''Click where the cursor is pointing.
        '''
        pos = queryMousePosition() # Query cursor position
        click(pos.x, pos.y) # Click
        return None

    @staticmethod
    def dist(x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


if __name__ == '__main__':
    M = Miner()
    M.main()
    

#Useful
#(58, 144, 76) <- surely part of the node, 18 matches - green name
#(146, 126, 134) <- diamond ore, possibly
