import os
import re
from pathlib import Path

import PySimpleGUI as sg

from scripts.launcher import Launcher
from scripts.fisher import Fisher
from tools import static
from tools.handler import validateLocalDataExistence, readLocalData, modifyLocalData

#----- Handle local data ----
validateLocalDataExistence()
local_data = readLocalData() 

def handlePath():
    '''Identify the name of the folder of the project and return
    the name as a string.
    '''
    return str(Path().absolute())

#----- GUI ELEMENTS -----

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

def output_window():
    '''Output window
    '''
    return sg.Output(size = (int(static.GUI_WIDTH/30), int(static.GUI_HEIGHT/40)))

def toggle_button(text:str, key:str):
    '''A button which toggles between colors when pressed.
    '''
    button = sg.Button(button_text=text, button_color=(sg.theme_button_color()),
            enable_events=True, key=key)
    return button 

#----- LOGIN WINDOW -----
def login_window():
    '''Return the sg.Frame of the login window.
    '''
    frame = sg.Frame(layout=[
            [sg.Text('Account name:', size = (14,1)),
                sg.Listbox(local_data.get('ACCOUNT_NAMES'), default_values = local_data.get('ACCOUNT_NAMES')[0],
                size = (18,1), key = '-ACCOUNT-NAMES-'),
                sg.Button('Edit', key = '-EDIT-ACCOUNT-NAMES-')
            ],
            [sg.Text('Character name:', size = (14,1)),
                sg.Listbox(local_data.get('CHARACTER_NAMES'), default_values = local_data.get('CHARACTER_NAMES')[0],
                size = (18,1), key = '-CHARACTER-NAMES-'),
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

def editAccountNames():
    '''Open up a popup window, display the current list of account names,
    and allow the user to input new values. If the names are modified,
    return those names as a list, otherwise return None.
    '''
    local_data = readLocalData()
    old_names = local_data.get('ACCOUNT_NAMES')
    def_text = 'Account1, Account2, ...' if old_names is None else ', '.join(old_names)
    msg = f"Insert new account names in the specified format.\nCurrent account names:\n"
    msg += "\n".join(old_names) # Each account name on a separate line
    new_names = sg.popup_get_text(message=msg, title='Edit Account Names', default_text=def_text,
        grab_anywhere=True, keep_on_top=False)
    if new_names is None:
        print("No changes made.")
        return None
    validation_regex = r'^\S[\w ]+(?:, \S[\w ]+)*$'
    new_names_validation = re.match(validation_regex, new_names)
    if not new_names_validation: # Invalid pattern
        print(f"\"{new_names}\" is an invalid input.\nPlease enter the account names in the format \"Acc1, Acc2\", and so on.")
        return None
    new_names_list = new_names.split(', ')
    modifyLocalData('ACCOUNT_NAMES', new_names_list)
    print(f"Account names changed to \"{new_names}\"")
    return new_names_list

def editCharacterNames():
    '''Similar to editAccountNames, only modify character names instead of 
    account names
    '''
    local_data = readLocalData()
    old_names = local_data.get('CHARACTER_NAMES')
    def_text = 'Character1, Character2, ...' if old_names is None else ', '.join(old_names)
    msg = f"Insert new account names in the specified format.\nCurrent character names:\n"
    msg += "\n".join(old_names) # Each character name on a separate line
    new_names = sg.popup_get_text(message=msg, title='Edit Character Names', default_text=def_text,
        grab_anywhere=True, keep_on_top=False)
    if new_names is None:
        print("No changes made.")
        return None
    validation_regex = r'^\S[\w ]+(?:, \S[\w ]+)*$'
    new_names_validation = re.match(validation_regex, new_names)
    if not new_names_validation: # Invalid pattern
        print(f"\"{new_names}\" is an invalid input.\nPlease enter the character names in the format \"Char1, Char2\", and so on.")
        return None
    new_names_list = new_names.split(', ')
    modifyLocalData('CHARACTER_NAMES', new_names_list)
    print(f"Character names changed to \"{new_names}\"")
    return new_names_list

def launchGameOnly(acc_name:str):
    '''Input the name of the account and launch the game with this account. No login.
    Invoked with the '-LAUNCH-GAME-' keyword from the main GUI window.
    '''
    L = Launcher()
    L.launch(acc_name)
    return None

def loginOnly(char_name:str):
    '''Input the name of the character and login with this character.
    '''
    L = Launcher()
    L.login(char_name)
    return None

def launchAndLogin(acc_name:str, char_name:str):
    '''Input the account name and the character name. Launch the game and login using
    said information.
    '''
    L = Launcher()
    L.launch(acc_name)
    L.login(char_name)
    return None

#----- FISHING -----

def fishInGUI(char_name:str, old_fish_timer):
    '''A master method for handling fishing.
    :arg:
        char_name (str) - Name of the character, which should do the fishing.
        fish_timer - Time, when the last fishing was initiated.
    '''
    try:
        F = Fisher(char_name)
    except:
        pass # Handle this later - game not on
    state = F.checkFishingState()
    outcome, new_fish_timer = F.handleFishingState(state, old_fish_timer)
    return outcome, new_fish_timer


#----- MINING -----
def mineInGUI(char_name:str):
    '''A master method for handling mining.
    '''
    pass
