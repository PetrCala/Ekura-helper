import time

from ctypes import windll
from pynput.keyboard import Key, HotKey, Controller
import pytesseract #Text recognition
import win32.win32gui as win32gui

from scripts.base import Base
from tools import static
from tools.handler import validateLocalDataExistence, readLocalData, getTesseractPath

windll.user32.SetProcessDPIAware() #Make windll properly aware of your hardware
pytesseract.pytesseract.tesseract_cmd = getTesseractPath() # Pytesseract path
keyboard = Controller()

#----- Handle local data ----
validateLocalDataExistence()
local_data = readLocalData()

class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()

class Launcher(Base):
    def __init__(self):
        pass

    def main(self):
        self.launch()

    @property
    def screen_pos(self):
        '''Position of the launcher. Kept as a property, in order to allow for opening
        of the launcher window after constructing the class.
        '''
        hwnd = self.getLauncherHwnd()
        return hwnd if hwnd is None else self.getWindowCoords(hwnd)

    def getLauncherHwnd(self):
        '''Get window handle number of the game launcher window.
        '''
        return self.getWindowHwnd(static.LAUNCHER_WINDOW_NAME)

    def getLauncherCoords(self):
        '''Get coordinates of the game launcher window. Added for more explicity.
        '''
        return self.screen_pos

    def openGameLauncher(self):
        '''Open the game launcher.
        '''
        self.useKey(Key.cmd, sleep = 0.2)
        self.useKeys(static.LAUNCHER_APP_NAME, sleep_after=0.3) # Write the game launcher name
        self.useKey(Key.enter, sleep = 0.9)
        tries = 0 # Placeholder for the upper limit on the window opening wait time
        hwnd = self.getLauncherHwnd()
        while hwnd is None and tries < 20: # Requires manual input for the UAC
            time.sleep(0.5) # Wait for the window to open
            hwnd = self.getLauncherHwnd()
            tries += 1
        if hwnd is None:
            print('Could not open the launcher window')
            return False
        time.sleep(3) # Wait for the launcher animations to finish
        x_scale, y_scale = static.MONITOR_LAUNCHER_DEFAULT_COORD[0:2]
        [x_abs, y_abs] = self.calculateCoords([x_scale, y_scale], from_scale=True, screen_pos_=self.monitor_coords)
        width_ = int(self.screen_pos[2] - self.screen_pos[0])
        height_ = int(self.screen_pos[3] - self.screen_pos[1])
        win32gui.MoveWindow(hwnd, x_abs, y_abs, width_, height_, False) # Move the window to the default coordinates
        print('Launcher open')
        return True

    def closeGameLauncher(self):
        '''Close the game launcher.
        '''
        hwnd = self.getLauncherHwnd()
        if hwnd is None: # Launcher not open
            return True 
        win32gui.CloseWindow(hwnd)
        return True

    def correctNameEntered(self, acc_name:str):
        '''Check whether there is not already the correct name input by default.
        If yes, return this name, if not, return False.
        '''
        window_text = self.readTextInRange(static.LAUNCHER_NAME_COORD)
        if acc_name == window_text.strip():
            return True
        return False

    def deleteName(self):
        '''Click into the name window and delete whatever is in there.
        '''
        x_, y_ = static.LAUNCHER_NAME_POS # Name window pos
        self.moveClick(x_, y_, from_scale = True)
        self.useKey(Key.ctrl, method='press', sleep=False)
        self.useKeys([Key.home, Key.delete])
        self.useKey(Key.ctrl, method='release', sleep=False)
        return True

    def inputName(self, acc_name:str):
        '''Input the account name into the game launcher. Assumer the launcher is
        already open. Return True, if the name was already correct, and False,
        if it had to be put in (focus is on the name window).
        '''
        if self.correctNameEntered(acc_name):
            print('The correct name is already in the launcher.')
            return True
        self.deleteName() # Delete the faulty name
        self.useKeys(acc_name) # Write the name
        return False

    def inputPassword(self):
        '''Input the character password into the game launcher. Assume the launcher is
        already open.
        '''
        x_, y_ = static.LAUNCHER_PW_POS # Password window
        self.moveClick(x_, y_, from_scale=True)
        self.useKeys(local_data.get('ACCOUNT_PASSWORD'))
        return True

    def launch(self, acc_name:str):
        '''Input the name, password, and start the game. The game launcher window
        must be open already.
        '''
        if not self.checkLauncherOpen():
            self.openGameLauncher()
        self.focusGameLauncher() # Put game launcher window into foreground
        self.inputName(acc_name)
        self.inputPassword()
        self.useKey(Key.enter, sleep = False) # Press 'start game' (may be changed to click)
        return True

    def checkLauncherOpen(self):
        '''Check whether the game launcher is open or not. If yes,
        return True. If not, return False.
        '''
        hwnd = self.getLauncherHwnd()
        if hwnd is None:
            return False
        return True

    def focusGameLauncher(self):
        '''Put the game launcher into foreground.
        '''
        hwnd = self.getLauncherHwnd()
        return win32gui.SetForegroundWindow(hwnd)
    
    def login(self, char_name:str):
        '''Input the name of the character to login with, choose that character out of the
        4 slots, and start the game with that character. Assume the character selection
        window is already open.
        '''
        pass