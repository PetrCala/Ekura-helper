﻿import time

import PySimpleGUI as sg

from scripts.launcher import Launcher
from scripts.fisher import Fisher
from scripts.miner import Miner
from tools import guitools as gt
from tools import static
from tools.handler import validateLocalDataExistence, readLocalData, modifyLocalData

#----- Handle local data ----
validateLocalDataExistence()
local_data = readLocalData()

class GUI:
    '''Graphical user interface
    '''
    def __init__(self):
        #File path handling
        self.base_path = gt.handlePath()

    def main(self):
        '''The main method for initiating the graphical user interface
        '''
        main_w = self.mainWindow()

        while True:
            window, event, values = sg.read_all_windows()
            #print(event, values)

            #------ Main window events ------
            if event in (sg.WINDOW_CLOSED, '-BACK-', 'Quit'):
                window.close()
                break

            #------ Login events ------
            elif event == '-EDIT-ACCOUNT-NAMES-':
                self.editAccountNames()

            elif event == '-EDIT-CHARACTER-NAMES-':
                self.editCharacterNames()

            elif event == '-LAUNCH-GAME-ONLY-':
                acc_name = values['-ACCOUNT-NAME-'][0]
                self.launchGameOnly(acc_name)

            elif event == '-LOGIN-ONLY':
                char_name = values['-CHARACTER-NAME-'][0]
                self.loginOnly(char_name)

            elif event == '-LAUNCH-AND-LOGIN-':
                acc_name = values['-ACCOUNT-NAME-'][0]
                char_name = values['-CHARACTER-NAME-'][0]
                self.launchAndLogin(acc_name, char_name)

            #------ Timer events ------
            elif event == '-START-TIMER-':
                self.startTimer()

            #------ Miner events -----

            #----- Fisher events -----

        return None

    def mainWindow(self):
        '''Open the main window of theGUI.
        '''
        sg.theme(static.GUI_THEME)
        sg.set_options(font=(static.GUI_FONT,static.GUI_FONT_SIZE))


        col_left_layout = [
                [self.loginWindow()]
            ]
        col_middle_layout = [[sg.Frame(layout = [
                    [sg.Text('hello')]
                ],
                title = 'Middle column')
        ]]
        col_right_layout = [[sg.Frame(layout = [
                    [sg.Text('hello')]
                ],
                title = 'Right column')
        ]]

        col_left = gt.main_col(col_left_layout)
        col_middle = gt.main_col(col_middle_layout)
        col_right = gt.main_col(col_right_layout)

        layout = [[col_left, col_middle, col_right]]

        return sg.Window(static.APP_NAME, layout, size = (static.GUI_WIDTH,static.GUI_HEIGHT), finalize=True)

    @staticmethod
    def loginWindow():
        '''Return the sg.Frame of the login window.
        '''
        frame = sg.Frame(layout=[
                [sg.Text('Account name:', size = (14,1)),
                 sg.Listbox(local_data.get('ACCOUNT_LIST'), default_values = local_data.get('ACCOUNT_LIST')[0],
                    size = (18,1), key = '-ACCOUNT-NAME-'),
                 sg.Button('Edit', key = '-EDIT-ACCOUNT-NAMES-')
                ],
                [sg.Text('Character name:', size = (14,1)),
                 sg.Listbox(local_data.get('CHARACTER_LIST'), default_values = local_data.get('CHARACTER_LIST')[0],
                    size = (18,1), key = '-CHARACTER-NAME-'),
                 sg.Button('Edit', key = '-EDIT-CHARACTER-NAMES-')
                ],
                [sg.Column([[
                    sg.Button('Launch', key = '-LAUNCH-GAME-ONLY-'),
                    sg.Button('Login', key = '-LOGIN-ONLY-'),
                    sg.Button('Launch and login', key = '-LAUNCH-AND-LOGIN-')
                    ]], justification = 'center')
                ]
            ]
            ,title = 'Login'
        )
        return frame

    @staticmethod
    def editAccountNames():
        '''Open up a popup window, display the current list of account names,
        and allow the user to input new values. Close the window at the end,
        and return None.
        '''
        pass

    @staticmethod
    def editCharacterNames():
        '''Similar to editAccountNames, only modify character names instead of 
        account names
        '''
        pass

    @staticmethod
    def launchGameOnly(acc_name:str):
        '''Input the name of the account and launch the game with this account. No login.
        Invoked with the '-LAUNCH-GAME-' keyword from the main GUI window.
        '''
        L = Launcher()
        L.launch(acc_name)
        return None
    
    @staticmethod
    def loginOnly(char_name:str):
        '''Input the name of the character and login with this character.
        '''
        L = Launcher()
        L.login(char_name)
        return None

    @staticmethod
    def launchAndLogin(acc_name:str, char_name:str):
        '''Input the account name and the character name. Launch the game and login using
        said information.
        '''
        L = Launcher()
        L.launch(acc_name)
        L.login(char_name)
        return None

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
