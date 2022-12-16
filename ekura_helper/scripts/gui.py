import sys
import os
import re
import numpy as np
import time
from datetime import datetime

import PySimpleGUI as sg

from tools import guitools as gt
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

    @staticmethod
    def startTimer(timer_time:int=3600):
        '''Start a timer in a separate window.
        '''
        # Create a progress bar to show the remaining time
        progress_bar = sg.ProgressBar(timer_time, orientation='h', size=(20, 20), key='progress')
        now = time.strftime("%H:%M")

        # Create a layout with the progress bar and a Cancel button
        layout = [[sg.Text(f'Started: {now}', size=(15,1), font='Helvetica', justification='left')],
                [sg.Text('', size=(15, 1), font=('Helvetica'), justification='left', key='time')],
                [progress_bar],
                [sg.B('Modify', button_color=('white', '#001480'), key = 'Modify'),
                sg.Exit(button_color=('white', 'firebrick4'), key = 'Exit')]]

        # Create a window with the above layout
        window = sg.Window('Timer', layout, auto_size_buttons=False, keep_on_top=False, grab_anywhere=True)

        # Main loop
        cancelled = False
        start_time = int(round(time.time()))
        remaining_time = timer_time

        while (True) and remaining_time > 0:
            event, values = window.read(timeout=10)
            elapsed_time = int(round(time.time())) - start_time
            remaining_time = timer_time - elapsed_time

            if event == 'button':
                event = window['event'].GetText()

            if event in (sg.WIN_CLOSED, 'Exit'):
                cancelled = True
                break
            elif event == 'Modify':
                wait_time = sg.popup_get_text('Enter number of seconds to wait:', grab_anywhere=True, keep_on_top=True)
                if int(wait_time) > timer_time:
                    raise ValueError('The wait time must be one hour at most.')
                remaining_time = int(wait_time)
                start_time = int(round(time.time())) - timer_time + remaining_time

            # Update the time
            window['time'].update('Remaining: {:02d}:{:02d}'.format(remaining_time // 60,
                                                            remaining_time % 60))

            # Update the progress bar with the remaining time
            window['progress'].UpdateBar(elapsed_time)

        # If the timer wasn't cancelled, show a popup with a message
        if not cancelled:
            sg.Popup('Timer finished!')
        window.Close()
        return None

    def mainWindow(self):
        '''Open the main window of theGUI.
        '''
        col1 = sg.Column([[sg.Text('1 hour timer:', size = (15,1), justification='left')],
                            [sg.Button('Timer', key='-START-TIMER-')]])

        layout = [[col1]]

        sg.theme(self.theme)
        sg.set_options(font=('Arial',10))
        return sg.Window('Ekura helper', layout, size = (1080,820), finalize=True)

    def main(self):
        '''The main method for initiating the graphical user interface
        '''
        main_w = self.mainWindow()

        while True:
            window, event, values = sg.read_all_windows()
            #print(event, values)

            if event in (sg.WINDOW_CLOSED, '-BACK-', 'Quit'):
                window.close()
                break

            elif event == '-START-TIMER-':
                self.startTimer()

        return None
