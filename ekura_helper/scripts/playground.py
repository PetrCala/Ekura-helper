from ctypes import windll
from pynput.keyboard import Controller
import pytesseract #Text recognition

from scripts.base import Base
from scripts.launcher import Launcher
from scripts.miner import Miner
from scripts.screenalysis import Screenalysis
from tools import static
from tools.handler import getTesseractPath

windll.user32.SetProcessDPIAware() #Make windll properly aware of your hardware
pytesseract.pytesseract.tesseract_cmd = getTesseractPath() # Pytesseract path
keyboard = Controller()

def test():
    B = Base()
    # M = Miner(char_name = local_settings.MINER_CHAR_NAME)
    L = Launcher()

    # Get coordinates (scaled) for the game launcher on the whole monitor
    # game_coords = L.getLauncherCoords()
    # x = B.calculateCoords(coords = game_coords[0:2], from_scale=False)
    # y = B.calculateCoords(coords = game_coords[2:4], from_scale=False)
    # print(x +  y)

if __name__ == '__main__':
    test()

