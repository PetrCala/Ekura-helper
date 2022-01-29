import numpy as np
from PIL import ImageGrab
import cv2
from directKeys import click, queryMousePosition, PressKey, ReleaseKey, SPACE
import time
import math


mouse_pos = queryMousePosition()

if __name__ == '__main__':
    print(f"Hello world!") 