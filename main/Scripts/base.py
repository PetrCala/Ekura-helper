from ctypes import windll
import cv2
from PIL import ImageGrab
from cv2 import mean #Capturing screen
from pynput.keyboard import Key, HotKey, Controller
import pytesseract #Text recognition

from .directKeys import click, queryMousePosition, PressKey, ReleaseKey, moveMouseTo
from .static import *

import numpy as np
import time
import math
import sys

windll.user32.SetProcessDPIAware() #Make windll properly aware of your hardware
pytesseract.pytesseract.tesseract_cmd = PYTESSERACT_PATH # Pytesseract path
keyboard = Controller()

class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()

class Base():
    def __init__(self):
        pass

    def main(self):
        '''Main method of the Base class
        '''
        pass

    @property
    def numbers(self):
        '''A list of the 10 roman numbers as strings. Used for keyboard input.
        '''
        return [str(i) for i in range(11)]

    def calculateCoords(self, coords:list, from_scale = True):
        '''Input a list of scale coordinates and return a list of the actual coordinates
        for the user's screen. It is possible to calculate in reverse direction too.
        :args:
            scale_coords[list] - A list of two scale coordinates marking a certain point on
                the screen.
            from_scale[bool, optional] - If True, input scale coordinates and return the actual
                coordinates on user's screen. If False, do the inverse. Defaults to True.
            
        :note:
            Scale coordinates - An initial point of [0.5,0.5] marks a point in the middle of the screen.
                In other words, it is 50 percent from top left corner in either direction.
            Actual coordinates - Actual pixels of the screen, such as [1000,500].
            Also assumes the game covers all of the screen, and does not move. Might change later.
        '''
        if not len(coords) == 2:
            raise ValueError('The coordinates must be input as a list of length 2')
        x_inp, y_inp = coords
        screen_width, screen_height = self.screen_size
        if from_scale:
            x = int(screen_width * x_inp) # Distance from left bound - x axis
            y = int(screen_height * y_inp) # Distance from upper bound - y axis
        else:
            x = round(x_inp/screen_width, 3)
            y = round(y_inp/screen_height, 3)
        return [x, y]

    def rangeToPixels(self, range:list):
        '''Specify a list of 4 scale coordinates and return a list of four points,
        which define (in pixels) the top left and bottom right points
        of the range, respectively.

        Args:
            range (list): List of four points of the range, in scale.
        '''
        if not len(range) == 4:
            raise ValueError('You must specify the range as a list of four points')
        start_ = range[0:2]
        end_ = range[2:4]
        start = self.calculateCoords(start_)
        end = self.calculateCoords(end_)
        return start + end

    def readTextInRange(self, range:list, lang:str = 'ces', view_range:bool = False):
        '''Specify as a list of scale coordinates the range in which
        a text should be recognized and return the text as a string.
        Args:
            range (list) - A list of scale coordinates.
            lang (str) - Language of the text in the range. Defaults to 'ces' (Czech).
            view_range (bool, optional) - If True, also open the screen.
                Defaults to False.
        '''
        range_pixels = self.rangeToPixels(range)
        img = self.createScreen(range_pixels, color_scale='orig')
        if view_range:
            self.openScreen(range_pixels, color_scale = 'orig')
        return pytesseract.image_to_string(img, lang = lang, config = TESSDATA_DIR_CONFIG)

    def createScreen(self, screen_pos:list = None, color_scale = 'gray'):
        '''Return a numpy array representing pixels on a screen. Specify the range
        of the screen with "screen_pos".
        :args:
            screen_pos[list] - A list of 4 integers specifying the range where
                the screen should be taken. Defaults to None (whole screen).
            color_scale[str] - Color scale which the screenshot should take.
                Can be set to 'gray', 'orig'.
        '''
        if screen_pos is None:
            screen_pos = self.screen_pos # Default to the whole screen
        if not len(screen_pos) == 4:
            raise ValueError('The screen_pos argument must be a list of length 4')
        screen = np.array(ImageGrab.grab(bbox=screen_pos))
        if color_scale == 'gray':
            return cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        elif color_scale == 'orig':
            return cv2.cvtColor(screen, cv2.COLOR_BGR2RGB) #Original color scale
        raise ValueError('The color_scale argument is misspecified.')

    def openScreen(self, screen_pos:list = None, win_name:str = 'Ekura screenshot', color_scale = 'gray'):
        '''Open the screenshot for viewing.
        :args:
            win_name[str] - Name of the window.
            screen_pos[list, optional] - List of coordinates where the screenshot
                should be taken. If None, use the whole game screen. Defaults to None.
        '''
        scale = 1
        if screen_pos is None:
            screen_pos = self.screen_pos
            scale = 0.9 # Resize if fullscreen
        screen = self.createScreen(screen_pos, color_scale=color_scale) #Take a screenshot
        window_width = screen_pos[2] - screen_pos[0]
        window_height = screen_pos [3] - screen_pos[1]
        window_res = [int(window_width*scale), int(window_height*scale)] # Window resizing
    
        cv2.namedWindow(win_name, cv2.WINDOW_NORMAL) # Create a Named Window
        cv2.moveWindow(win_name, 0, 0) # Move it to (X,Y)
        cv2.imshow(win_name, screen) # Show the Image in the Window
        cv2.resizeWindow(win_name, window_res[0], window_res[1])   # Resize the Window
        cv2.waitKey(0); cv2.destroyAllWindows(); cv2.waitKey(1) #Handle closing of the window
        return None

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
        print(f'Searching for pixel with rgb values from {rgb}...')
        screen = self.createScreen(color_scale = 'orig') #Take a snapshot of the screen
        match_count = 0
        match_list = []
        start_time = time.time()
        for y in range(self.screen_size[1]):
            for x in range(self.screen_size[0]):
                pixel_rgb = screen[y,x].tolist()
                if pixel_rgb in rgb:
                    match_count = match_count + 1
                    # print(f'Found a match at position ({x}, {y})')
                    match_list.append([x,y])
        search_time = round(time.time() - start_time, 2)
        print(f'Search complete.\nFound {match_count} matching pixels.\nThe search took {search_time} seconds.')
        return match_list

    def getMousePosition(self, scale = False, verb = False):
        '''Get the coordinates of the current mouse position.
        
        Arg:
            scale [bool] - If True, return/print the coordinates as a scale.
            verb [bool] - If True, only print out the output. If False, return the output
                as a list of coordinates.
        '''
        m = queryMousePosition()
        x = m.x
        y = m.y
        if scale:
            x, y = self.calculateCoords([x,y], from_scale = False) # Absolute coordinates to scale
        if verb:
            print(f'The mouse position is\nx:{x}\ny:{y}')
            return None
        return [x,y]
    
    def num_key(self, key):
        '''Convert the string corresponding to a roman number to a key code legible by the keyboard.
        '''
        if not key in self.numbers:
            raise ValueError('Only roman numbers can be converted.')
        return keyboard._KeyCode(char = key)
        
    def useKeys(self, keys):
        '''For each key in keys, press this key. Keys can be any iterable object.
        '''
        for key in keys:
            self.useKey(key)
        return None

    def useKey(self, key):
        '''An extended method for handling more complex key pressing.
        :args:
            key - Key to be pressed. Accepts all inputs of pynput, along with roman numbers in a string form (i.e. '5').
            method[str] - Method by which the key shall be used. Must be an attribute of the keyboard.
            sleep[bool] - If true, insert a 0.2 sleep time after the key press. Defaults to True.
        '''
        if not key in KEYS.keys():
            raise ValueError('This key cannot be pressed')
        if key in self.numbers:
            key = self.num_key(key) #Parse a roman number
        key_hx = KEYS.get(key) 
        PressKey(key_hx)
        time.sleep(1)
        ReleaseKey(key_hx)
        return None

    @staticmethod
    def checkStringForMatches(input_string:str, match_list:list, verbose:bool = False):
        '''Input a string, and a list of words to look for, and return the number
        of matches found in the string for said list.

        Args:
            input_string (str): String to search for potential matches.
            match_list (list): List of words to search for in the string.
            verbose (bool): If True, print out a message with the number of matches.

        Returns:
            int: The number of matches found in the string.
        '''
        matches = 0
        input_words = input_string.split()
        for word in input_words:
            if word in match_list:
                matches += 1
        if verbose:
            plural = 'es' if matches != 1 else ''
            print(f'Found {matches} match{plural}.')
        return matches

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

    @classproperty
    def screen_pos(cls):
        '''
        Return a list of 4 coordinates marking the beginning and end of the screen
            in the form [x1,y1, x2, y2].
        '''
        return [0,0] + cls.screen_size

    @classproperty
    def screen_size(cls):
        '''
        A static property defining the screen resolution.
        
        :return:
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
    B = Base()
    B.main()
