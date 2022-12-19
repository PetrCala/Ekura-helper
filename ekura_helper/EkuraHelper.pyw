from ctypes import windll
from pynput.keyboard import Controller
import pytesseract #Text recognition

from scripts.gui import GUI
from scripts.launcher import Launcher
from scripts.fisher import Fisher
from scripts.miner import Miner
from tools.handler import validateLocalDataExistence, readLocalData, getTesseractPath

#----- Handle keyboard input and screen capture -----
windll.user32.SetProcessDPIAware() #Make windll properly aware of your hardware
pytesseract.pytesseract.tesseract_cmd = getTesseractPath('exe') # Pytesseract path to executable
TESSDATA_DIR_CONFIG = getTesseractPath('conf') # Pytesseract path to config file
keyboard = Controller()

#----- Handle local data ----
validateLocalDataExistence()
local_data = readLocalData()

#----- Main -----
def main():
    #----- Run GUI -----
    G = GUI()
    G.main()

    #----- Fish -----
    # F = Fisher(char_name = 'Stand')
    # F.main()


    #----- Mine -----
    # M = Miner(char_name = localsettings.CHAR_NAME)
    # M.main() # Mine

    #----- Launch the game -----
    # L = Launcher()
    # L.launch('Bloodbath')


if __name__ == '__main__':
    main() 