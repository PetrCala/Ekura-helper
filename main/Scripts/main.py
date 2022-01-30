import numpy as np
from PIL import ImageGrab
import cv2
from directKeys import click, queryMousePosition, PressKey, ReleaseKey, moveMouseTo, SPACE
import time
import math



mouse_pos = queryMousePosition()
#return { "x": pt.x, "y": pt.y}/

def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)





if __name__ == '__main__':
    moveMouseTo(100,100)