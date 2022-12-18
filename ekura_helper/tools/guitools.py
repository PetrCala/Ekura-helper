import os
from pathlib import Path

import PySimpleGUI as sg

from tools import static

def handlePath():
    '''Identify the name of the folder of the project and return
    the name as a string.
    '''
    return str(Path().absolute())

def main_col(input_layout:list):
    '''One of the three main columns of the GUI.
    Input a nested list.
    '''
    col = sg.Column(
        layout = input_layout,
        size = (static.GUI_WIDTH/3, static.GUI_HEIGHT),
        justification = 'center'
        )
    return col