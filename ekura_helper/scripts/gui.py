import time
import re

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
        bot_buttons = {'-TOGGLE-FISHING-': False, '-TOGGLE-MINING-': False}
        bot_fish_timer = time.time() - 99 # Arbitrary timestamp

        main_w = self.mainWindow()

        while True:
            window, event, values = sg.read_all_windows()
            #print(event, values)

            #----- State of bot actions -----
            fishing_on = bot_buttons.get('-TOGGLE-FISHING-')
            mining_on = bot_buttons.get('-TOGGLE-MINING-')
            bot_state = [fishing_on, mining_on]
            bot_idle = not any(bot_state)

            #------ Main window events ------
            if event in (sg.WINDOW_CLOSED, '-BACK-', 'Quit'):
                window.close()
                break

            #------ Login events ------
            elif event == '-EDIT-ACCOUNT-NAMES-':
                new_names_list = gt.editAccountNames()
                window['-ACCOUNT-NAMES-'].update(new_names_list)

            elif event == '-EDIT-CHARACTER-NAMES-':
                new_names_list = gt.editCharacterNames()
                window['-CHARACTER-NAMES-'].update(new_names_list)

            elif event == '-LAUNCH-GAME-ONLY-':
                acc_name = values['-ACCOUNT-NAMES-'][0]
                gt.launchGameOnly(acc_name)

            elif event == '-LOGIN-ONLY':
                char_name = values['-CHARACTER-NAMES-'][0]
                gt.loginOnly(char_name)

            elif event == '-LAUNCH-AND-LOGIN-':
                acc_name = values['-ACCOUNT-NAME-'][0]
                char_name = values['-CHARACTER-NAME-'][0]
                gt.launchAndLogin(acc_name, char_name)

            #------ Timer events ------
            elif event == '-START-TIMER-':
                self.startTimer()

            #------ Miner events -----

            #----- Fisher events -----
            elif event == '-TOGGLE-FISHING-':
                if (not bot_buttons[event]) and (not bot_idle): # Bot already working
                    print('You must turn off the bot\'s other action first.')
                else: # Check passed    
                    bot_buttons[event] = not bot_buttons[event] # Change button state
                    if bot_buttons[event]:
                        window[event].update(button_color='light grey')
                    else:
                        window[event].update(button_color=sg.theme_button_color())

            #----- Bot actions -----
            if sum(bot_state) > 2:
                raise SystemError('The bot must never be allowed to perform more than 1 action at once.')
            elif sum(bot_state) == 1:
                char_name = values['-CHARACTER-NAMES-'][0]
                if fishing_on:
                    if time.time() - bot_fish_timer > 0.5: # Check interval
                        outcome, new_fish_timer = gt.fishInGUI(char_name, bot_fish_timer)
                        if outcome is False: # Turn the fishing off
                            bot_buttons['-TOGGLE-FISHING-'] = False
                            window[event].update(button_color=sg.theme_button_color())
                        if new_fish_timer is not None:
                            bot_fish_timer = new_fish_timer # Update the timer since last fishing
                elif mining_on:
                    gt.mineInGUI(char_name)

        return None

    def mainWindow(self):
        '''Open the main window of theGUI.
        '''
        sg.theme(static.GUI_THEME)
        sg.set_options(font=(static.GUI_FONT,static.GUI_FONT_SIZE))


        col_left_layout = [
                [gt.login_window()]
            ]
        col_middle_layout = [[sg.Frame(layout = [
                    [gt.output_window()]
                ],
                title = 'Output')
        ]]
        col_right_layout = [[sg.Frame(layout = [
                    [gt.toggle_button('Fishing', key = '-TOGGLE-FISHING-')]
                ],
                title = 'Fishing')
        ]]

        col_left = gt.main_col(col_left_layout)
        col_middle = gt.main_col(col_middle_layout)
        col_right = gt.main_col(col_right_layout)

        layout = [[col_left, col_middle, col_right]]

        return sg.Window(static.APP_NAME, layout, size = (static.GUI_WIDTH,static.GUI_HEIGHT), finalize=True)


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
