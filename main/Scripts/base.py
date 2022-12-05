from ctypes import windll
import cv2
from PIL import ImageGrab
from cv2 import mean #Capturing screen
from pynput.keyboard import Key, HotKey, Controller
import pytesseract #Text recognition
import pywintypes
import win32.win32gui as win32gui

from static import *
# from main.local_settings import *
from directKeys import click, queryMousePosition, PressKey, ReleaseKey, moveMouseTo

import numpy as np
import random
from datetime import datetime, timedelta
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

class Base():
    def __init__(self):
        '''Constructor for the base class.
        '''
        pass

    def main(self):
        '''Main method of the Base class
        '''
        pass

    @property
    def screen_pos(self):
        '''
        Return a list of 4 coordinates marking the beginning and end of the screen
            in the form [x1,y1, x2, y2]. Specified as a property in order to allow
            overriding when input needs to be sent to a different window (such as
            when logging in).
        '''
        pos = self.getGameCoords() # Throws an error if game is not running
        return pos

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
        current_screen = self.screen_pos
        screen_width = current_screen[2] - current_screen[0]
        screen_height = current_screen[3] - current_screen[1]
        if from_scale:
            # Take left/top edge, and add the desired distance (percentage of screen) to get coord
            x = int(current_screen[0] + screen_width * x_inp) # x axis
            y = int(current_screen[1] + screen_height * y_inp) # y axis
        else:
            # Take pixels from edge to coord, then calculate what percentage of screen
            # that distance covers
            x = round((x_inp - current_screen[0])/screen_width, 3)
            y = round((y_inp - current_screen[1])/screen_height, 3)
        return [x, y]

    def validateGamePos(self):
        '''Check that the game window is in a position where all important inputs can be read.
        '''
        print('Validating game position...')
        start_time = time.time()
        screen_pos = self.screen_pos # Actual game position
        monitor_pos = self.monitor_coords # Monitor position
        x_verify, y_verify = [], [] # Coordinates to be verified
        for coords in VALIDATION_COORDS:
            x_verify = x_verify + [coords[0], coords[2]]
            y_verify = y_verify + [coords[1], coords[3]]
        # Absolute coordinates       
        x_abs = [self.calculateCoords([coord,0])[0] for coord in x_verify]
        y_abs = [self.calculateCoords([0,coord])[1] for coord in y_verify]
        # Check if all coordinates are valid
        x_valid = all([monitor_pos[0] < coord < monitor_pos[2] for coord in x_abs])
        y_valid = all([monitor_pos[1] < coord < monitor_pos[3] for coord in y_abs])
        if not x_valid and y_valid:
            raise SystemError('Some crucial parts of the game window are hidden. Please recenter the game window.')
        # Possibly move the game automatically to a pre-defined location, if it makes more sense
        validation_time = round(time.time() - start_time, 2)
        print(f'The game position is valid. The validation took {validation_time} seconds.')
        return True

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

    def pixelsOnScreen(self, rgb:list, range_coords:list = None):
        '''
        Enter the r,g,b value of desirable pixel values and return a list with coordinates
            where these match on the screen. Search range can be specified, defaults to whole screen.

        Arg:
            rgb [list] - This must be a nested list of possible rgb combinations, which should be
                searched.
            range_coords [list] - Range, which should be checked, given by 4 coordinates. Defaults to None,
                in which case the whole screen is checked.

        Returns:
            [list]: A list of the coordinates where the match was found
        '''
        assert any(isinstance(i, list) for i in rgb), 'The argument must be a nested list'
        print(f'Searching for pixels...')
        if range_coords is None:
            range_coords = self.screen_pos
        screen = self.createScreen(screen_pos = range_coords, color_scale = 'orig') #Take a snapshot of the range/screen
        match_list = []
        width = range_coords[2] - range_coords[0]
        length = range_coords[3] - range_coords[1]
        start_time = time.time()
        for y in range(length - 1): # Last subscript is out of bounds -> don't check it
            for x in range(width - 1):
                pixel_rgb = screen[y,x].tolist()
                if pixel_rgb in rgb:
                    match_list.append([x,y])
        search_time = round(time.time() - start_time, 2)
        match_count = len(match_list)
        print(f'Found {match_count} matching pixels.\nThe search took {search_time} seconds.')
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
        return x,y
    
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

    def getGameHwnd(self):
        '''Return the hwnd of the main game window. If not open, throw a system error.
        '''
        lookup_words = [GAME_WINDOW_NAME, MINER_CHAR_NAME] # Game window name
        hwnd = self.getWindowHwnd(lookup_words)
        if hwnd is None:
            raise SystemError('The game is not running. Start the game first')
        return hwnd

    def getGameCoords(self):
        '''Return the coordinates of the game window as a list of 4 coordinates.
        '''
        hwnd = self.getGameHwnd()
        pos = win32gui.GetWindowPlacement(hwnd)
        return list(pos[4])

    def focusGame(self):
        '''Bring the game into focus.
        '''
        hwnd = self.getGameHwnd() # Automatically raises error if not found.
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.2) # Allow for smoother immediate input
        return True

    def focusedInput(self, input:str, window_hwnd:int = None):
        '''Main method for sending key input into game. Handles window focus, allows for
        single keys, or multiple keys.

        :arg:
            input (str) - The key(s) to be pressed in game/window.
            window_hwnd (int) - Window handle of the desired window.
        '''
        assert isinstance(input, str), 'The input must be a string.'
        active_hwnd = win32gui.GetForegroundWindow() # Focused window before input
        if window_hwnd is None:
            self.focusGame()
        else:
            win32gui.SetForegroundWindow(window_hwnd)
        if len(input) > 1:
            self.useKeys(input)
        else:
            self.useKey(input)
        win32gui.SetForegroundWindow(active_hwnd) # Return focus
        return True

    def focusedClick(self, x:int, y:int, window_hwnd:int = None):
        '''Click with focus handling.

        :arg:
            x,y (int) - Coordinates of the click
            window_hwnd (int) - Window handle of the desired window.
        '''
        active_hwnd = win32gui.GetForegroundWindow() # Focused window before input
        if window_hwnd is None:
            self.focusGame()
        else:
            win32gui.SetForegroundWindow(window_hwnd)
        self.moveClick(x, y)
        win32gui.SetForegroundWindow(active_hwnd) # Return focus
        return True

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
    def monitor_coords(cls):
        '''Coordinates of the monitor, which the game is allowed to be ran on.
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
    def moveClick(x, y):
        '''Specify coordinates and click there. Used for clicks in game,
        automaically adds a small wait window in order to guarantee the click.
        Returns the cursor back to the starting position.
        '''
        pos = queryMousePosition()
        x_, y_ = pos.x, pos.y # Initial mouse coordinates
        moveMouseTo(x, y)
        time.sleep(0.1) # Allow for cursor positioning
        click(x, y)
        moveMouseTo(x_,y_) # Return the mouse
        return None

    @staticmethod
    def randomizeClicking(x,y):
        '''Input the two coordinates and move each one by a small, random amount of pixels
        in a random direction. Return the new coordinates as a pair.
        '''
        scale1 = random.uniform(-5,5)
        scale2 = random.uniform(-5,5)
        x_ = int(x + scale1)
        y_ = int(y + scale2)
        return x_, y_

    @property
    def char_pos(self):
        '''Position of the character, given by two coordinates.
        '''
        raw_coords = self.readTextInRange(CHAR_POS_COORD)
        if not re.match(CHAR_POS_REGEX, raw_coords):
            raise ValueError('Could not identify the character\'s coordinates.')
        coords_set = re.match(CHAR_POS_REGEX_EXTRACT, raw_coords)
        coords = int(coords_set[1]), int(coords_set[2]) # x,y
        return coords
        
    @staticmethod
    def getWindowHwnd(lookup_words):
        '''Specify a window name and return its window handle. Allows regex patterns.
        :arg:
            lookup_words (str, or list) - Word/s that the window name must contain.
        :return:
            hwnd -  Handle of the said window.
        '''
        windows = []
        def callback(hwnd, extra):
            if isinstance(lookup_words, str):
                if lookup_words.upper() in win32gui.GetWindowText(hwnd).upper():
                    windows.append(hwnd)
            elif isinstance(lookup_words, list):
                if all([word.upper() in win32gui.GetWindowText(hwnd).upper() for word in lookup_words]):
                    windows.append(hwnd)
            else:
                raise ValueError('Specify either a single or multiple words that the window should contain.')
            return True
        win32gui.EnumWindows(callback, None)
        if windows == []: #Window not found
            return None
        elif len(windows) > 1:
            raise ValueError('Multiple windows open.')
        return windows[0]

    @staticmethod
    def dist(x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

if __name__ == '__main__':
    B = Base()
    B.main()
