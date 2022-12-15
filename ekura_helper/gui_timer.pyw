### A temporary .py script for running a timer ###

from datetime import datetime
import time

import PySimpleGUI as sg

from tools import static

# Get the user-specified time for the timer

def main():
    timer_time = 3600 # 1 hour timer

    layout = [[sg.Text('1 hour timer:', size = (15,1), justification='left')],
            [sg.Button('Start')]]

    window = sg.Window('Timer').Layout(layout)

    while True:
        event, values = window.Read()

        if event in (sg.WINDOW_CLOSED, 'Quit'):
            window.close()
            break

        # If the user clicks the Start button, start the timer
        if event == 'Start':
            start_timer(timer_time)

def start_timer(timer_time):
    '''Define a time in seconds, and open a window with a progress bar,
        which closes automatically after the timer runs out.
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

if __name__ == '__main__':
    main()