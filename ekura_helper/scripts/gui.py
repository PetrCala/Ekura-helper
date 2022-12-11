import sys
import os
import re
import numpy as np
import PySimpleGUI as sg

from tools import static

class GUI:
    '''Graphical user interface
    '''
    def __init__(self):
        #Defining file paths
        self.base_path = str(os.getcwd())
        self.theme = 'LightGrey1'
        # script_path = self.base_path + r'\scripts'
        
        # Path handling
        if not static.APP_FOLDER_NAME in self.base_path:
            raise SystemError('Folder name incorrect')
        # if script_path not in sys.path:
        #     sys.path.insert(0, script_path)

    def openInitW(self):
        '''Open the initial window of theGUI.
        '''
        col1 = sg.Column([[sg.Text('hello')]])

        layout = [[col1]]

        sg.theme(self.theme)
        sg.set_options(font=('Arial',10))
        return sg.Window('Ekura helper', layout, size = (1080,820), finalize=True)


    def main(self):
        '''The main method for initiating the graphical user interface
        '''
        init_w = self.openInitW()

        while True:
            window, event, values = sg.read_all_windows()
            #print(event, values)

            if event == sg.WINDOW_CLOSED or event == '-BACK-' or event == 'Quit':
                window.close()
                break

        return None
