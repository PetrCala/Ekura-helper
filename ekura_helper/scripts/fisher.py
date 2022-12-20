import pandas as pd
import random
from datetime import datetime, timedelta
import re
import time
from os.path import exists
from pathlib import Path

from ctypes import windll
from pynput.keyboard import Controller
import pytesseract #Text recognition

from scripts.base import InGameBot
from tools import static
from tools import settings
from tools.handler import getTesseractPath

windll.user32.SetProcessDPIAware() #Make windll properly aware of your hardware
pytesseract.pytesseract.tesseract_cmd = getTesseractPath() # Pytesseract path
keyboard = Controller()


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()

class Fisher(InGameBot):
    '''A class for automatic fishing. Assumes you have the fishing rod equipped.

    Args:
        InGameBot (_type_): _description_
    '''
    def __init__(self, char_name:str, *args, **kwargs):
        '''Constructor for the Fisher class. Game must be running in order for the
            constructor to be callable.

        Args:
            char_name (str): Name of the character which shall be operated by the bot.
        '''
        # Attributes
        self.check_interval = 0.5 # Float, amount of time to wait before checking fishing state
        self.fishing_timer = datetime.now() + timedelta(days = -1)
        # Constructor operations
        super(Fisher, self).__init__(char_name, *args, **kwargs) # Master class inheritance

    def main(self):
        '''Main method of the Miner clsass
        '''
        while True:
            if settings.PRODUCTION:
                state = self.checkFishingState()
                self.handleFishingState(state)
                time.sleep(self.check_interval)
            else:
                self.fishAWhile()


    def checkFishingState(self):
        '''Check the state of fishing and return an integer identifying said state.
        Game must be open.
        :legend:
            No message:
            0 - Fishing ongoing, or not fishing
            With message:
            1 - Fish escaped
            2 - Fish caught successfully
            3 - Fish on
            4 - Bait on
            5 - No bait on
            6 - Fishing impossible in this area
        '''
        msg = self.readTextInRange(static.MESSAGE_LOG_COORD, view_range=False)
        if self.checkStringForMatches(msg, static.FISHING_FISH_GONE_KEYWORDS) > 1:
            return 1
        if self.checkStringForMatches(msg, static.FISHING_FISH_CAUGHT_KEYWORDS, verbose = False) > 1:
            return 2
        if self.checkStringForMatches(msg, static.FISHING_FISH_ON_KEYWORDS, verbose = False) > 0:
            return 3
        if self.checkStringForMatches(msg, static.FISHING_LURE_ON_KEYWORDS, verbose = False) > 0:
            return 4
        if self.checkStringForMatches(msg, static.FISHING_NO_LURE_KEYWORDS, verbose = False) > 1:
            return 5
        if self.checkStringForMatches(msg, static.FISHING_IMPOSSIBLE_KEYWORDS, verbose = False) > 0:
            return 6
        return 0

    def handleFishingState(self, state:int, old_fish_timer):
        '''Take action based on the fishing state information.
        If the fishing is continuing well, return True.
        If the fishing is further impossible and should be terminated, return False.
        Also return a timestamp of now, if fishing was initiated, otherwise return None.
        :return:
            outcome, new_fish_timer [bool, time]
        '''
        new_fish_timer = None
        if state == 0:
            new_fish_timer = self.tryFishing(old_fish_timer)
            if not settings.PRODUCTION:
                print('Fish state checked...')
        elif state == 6:
            print('Fishing is impossible here.')
            return False, new_fish_timer
        elif state == 5:
            print('You have no bait on the rod.\nPutting on a bait...')
            bait_on = self.putOnBait()
            if not bait_on: # Impossible to put on a bait
                return False, new_fish_timer
        elif state == 4:
            print('Bait is on. Initiating fishing...')
            if old_fish_timer - time.time() > 20:
                self.focusedInput('SPACE')
                new_fish_timer = time.time()
        elif state == 3:
            self.pullUp()
        elif state == 2:
            print('Fish caught successfully.')
            time.sleep(1.5)
            new_fish_timer = self.tryFishing(old_fish_timer)
        elif state == 1:
            print('Fish escaped.')
            time.sleep(1.5)
            new_fish_timer = self.tryFishing(old_fish_timer)
        return True, new_fish_timer

    def tryFishing(self, old_fish_timer):
        '''Try to initate fishing. If successful, return a new fishing timer.
        Otherwise return None
        '''
        new_fish_timer = None
        if old_fish_timer - time.time() > 40:
            self.focusedInput('SPACE')
            print('Initiating fishing...')
            new_fish_timer = time.time()
        return new_fish_timer

    def putOnBait(self):
        '''Put on a bait. If the bait is put on successfully, return True,
        otherwise return False.
        '''
        time.sleep(0.2) # Allow for proper input
        self.focusedInput(static.FISHING_LURE_SLOT) # Put on lure
        time.sleep(0.5) # Allow for message to appear
        new_state = self.checkFishingState()
        if new_state != 4:
            print('Failed to put on lure.')
            return False
        return True

    def pullUp(self):
        '''Initiate after detecting a fish.
        '''
        msg = self.readTextInRange(static.MESSAGE_LOG_COORD, view_range=False)
        fish_type = self.readFishType(msg)
        wait_time = self.calculateFishWaitTime(fish_type)
        time.sleep(wait_time)
        print(f'Pulling up after {round(wait_time, 2)} seconds...')
        self.focusedInput('SPACE') # Pull up
        return None

    def fishAWhile(self):
        '''Perform several catches. Stop after a while.
        '''
        fishing_count = 0
        self.fishing_impossible = False # Allow for fishing to start
        while (not self.fishing_impossible) and (fishing_count <= 10):
            self.fishOutsideProduction()
            fishing_count += 1
        return True

    def fishOutsideProduction(self):
        '''Assuming all fishing requirements were fulfilled, start fishing.
        Return True if the fishing was successful, and False otherwise.
        '''
        time_checked = 0
        start = time.time()
        self.focusedInput('SPACE')
        time.sleep(0.4) # Wait for the message to appear
        we_fishing = self.checkIfFishingStarted()
        if we_fishing is False: # Start fishing (check automatically puts on lure)
            time.sleep(0.2) # Allow for proper refocusing
            self.focusedInput('SPACE')
        self.fishing_finished = False # Fishing started
        print('Initiating fishing...')
        time.sleep(10) # No fish in the first 10 seconds
        while (not self.fishing_finished) and (time_checked < 50):
            fishing_state = self.checkFishingProgress()
            if isinstance(fishing_state, str): # Fish caught
                print(f'{fishing_state} found. The wait took {round(time.time() - start, 2)} seconds.')
                wait_time = self.calculateFishWaitTime(fishing_state)
                time.sleep(wait_time)
                print(f'Pulling up after {round(wait_time, 2)} seconds...')
                self.focusedInput('SPACE') # Pull up
                time.sleep(2)
                if settings.PRODUCTION is False:
                    self.handleCatchResults(fish = fishing_state, time = wait_time)
                time.sleep(2) # Wait for the animations to finish
                self.fishing_finished = True
                print('Fish pulling complete.')
                return True
            time.sleep(self.check_interval) # Wait before checking again
            time_checked += 1
        print('Could not find any fish. Trying again...')
        return True

    def checkIfFishingStarted(self):
        '''Check all the necessary requirements to start fishing. If all are fulfilled,
        return True, else return False.
        '''
        msg = self.readTextInRange(static.MESSAGE_LOG_COORD, view_range=False)
        fishing_impossible = self.checkStringForMatches(msg, static.FISHING_IMPOSSIBLE_KEYWORDS, verbose = False)
        if fishing_impossible > 0:
            print('You can not fish here...')
            self.fishing_impossible = True
            return False
        no_lure = self.checkStringForMatches(msg, static.FISHING_NO_LURE_KEYWORDS, verbose = False)
        if no_lure > 1:
            time.sleep(0.2) # Allow for proper input
            print('No bait is on. Putting on bait...')
            self.focusedInput(static.FISHING_LURE_SLOT) # Put on lure
            time.sleep(0.3)
            new_msg = self.readTextInRange(static.MESSAGE_LOG_COORD, view_range = False)
            lure_on = self.checkStringForMatches(new_msg, static.FISHING_LURE_ON_KEYWORDS, verbose = False)
            if not lure_on > 0:
                print('Failed to put the bait on. Fishing impossible.')
                self.fishing_impossible = True
            return False
        self.fishing_impossible = False
        return True

    def checkFishingProgress(self):
        '''A method for periodically checking whether the fishing has finished yet.
        If a fish has been spotted, return a string with the name of the fish,
        otherwise return None.
        '''
        # If not fishing, set self.fishing_finished to False
        msg = self.readTextInRange(static.MESSAGE_LOG_COORD, view_range=False)
        msg_parts = msg.split()
        if ('že' in msg_parts) and ('právě' in msg_parts):
            fish_type = self.readFishType(msg)
            return fish_type
        fishing_failed = self.checkStringForMatches(msg, static.FISHING_FISH_GONE_KEYWORDS)
        if fishing_failed > 1:
            print('Failed to catch the fish.')
            self.fishing_finished = True
            time.sleep(4) # Waiting for the fishing state to reset
        return None
        
    def randomizeWaitTime(self, time:float):
        '''Input a float indicating fish wait time, and randomize it
        by shifting it several tenths of a second in either direction.
        Return the new time.
        :args:
            time (float): Time to wait.
        '''
        offset = random.uniform(-0.75, 0.75) 
        return time + offset
    
    def handleCatchResults(self, fish:str, time:float):
        '''Notes down the statistics, if the catch was successful.
        :arg:
            fish (str) - Name of the fish.
            time (float) - Time the character waited from the message detection
                until pulling the fish.
        '''
        msg = self.readTextInRange(static.MESSAGE_LOG_COORD)
        gone = self.checkStringForMatches(msg, static.FISHING_FISH_GONE_KEYWORDS)
        caught = self.checkStringForMatches(msg, static.FISHING_FISH_CAUGHT_KEYWORDS)
        if gone > 0: # Fish gone
            return None
        if caught > 1 and not settings.PRODUCTION: # Successful catch
            with open('fish_stats.txt', 'a') as f:
                f.write(f'Fish: {fish}, Wait time since message detection: {round(time,2)}s, Date: {datetime.now()}\n')
        return None

    @staticmethod
    def readFishType(msg:str):
        '''Input the message with the fish on the rod, return an integer
        indicating the seconds necessary.
        '''
        # Possibly change into regex later
        fish_list = []
        msg_parts = msg.split()
        idx_before = msg_parts.index('že') + 1
        idx_after = msg_parts.index('právě')
        for i in range(idx_before, idx_after):
            fish_list.append(msg_parts[i])
        fish_type = ' '.join(fish_list)
        if fish_type in static.FISHING_BOT_TYPOS.keys():
            typo = fish_type
            fish_type = static.FISHING_BOT_TYPOS.get(fish_type) # Get correct name
            if settings.PRODUCTION is False:
                with open('notes/fishtypos.txt', 'a') as f:
                    f.write(f'\'{typo}\': \'{fish_type}\',\n')
        return fish_type

    @staticmethod
    def calculateFishWaitTime(fish_name:str):
        '''Input a fish name and return its wait time.
        '''
        wait_random = random.uniform(1,6)
        res = next((sub for sub in static.FISHING_FISH_INFORMATION if fish_name in sub['Fish name']), None)
        if res is None:
            print(f'{fish_name} is not in our library... Let\'s wait randomly until pulling up')
            return wait_random
        # avg_ = res.get('Average')
        min_, max_ = res.get('Min'), res.get('Max')
        min_ = min_ if min_ != 0.0 else wait_random # No data
        max_ = max_ if max_ != 0.0 else wait_random # No data
        wait_time = random.uniform(min_ - min_/3, max_ + max_/3) # Add an offset to allow for data collection
        return round(wait_time, 2)

    @staticmethod
    def updateExcel():
        '''Read the text data file, preprocess the data, and update the 'data' sheet
        of the 'Fish data.xlsx' excel.
        '''
        abs_path = str(Path().absolute())
        source_path = abs_path + r'\fish_stats.txt'
        excel_path = abs_path + r'\notes\Fish data.xlsx'
        if not (exists(source_path) and exists(excel_path)):
            raise FileExistsError('A file has been misplaced.')
        with open(source_path) as f:
            source = f.readlines()
        out = []
        reg_ = 'Fish: (.*), Wait time since message detection: (.*)s, Date: (.*)'
        for fish_text in source:
            match = re.match(reg_, fish_text)
            temp_dict = {
                'Fish name': str(match[1]), 
                'Wait time': float(match[2]),
                'Date': pd.to_datetime(match[3]),
                }
            out.append(temp_dict)
        fish_df = pd.DataFrame(out)
        abs_path = str(Path().absolute())
        excel_path = abs_path + r'\notes\Fish data.xlsx'
        fish_df.to_excel(excel_path, sheet_name = 'Data', index = False)
        return source

    @staticmethod
    def convertExcelToDict(print_dict:bool=True):
        '''Load the fish data and transform it into data as a dictionary in the format
            {'Fish name': 'Losos', 'Average': 2.1, 'Min': 1.5, 'Max': 2.5}.
        :arg:
            print_dict(bool) - If True, print out the dictionary into the console.
        '''
        result = []
        path = str(Path().absolute()) + r'\notes\Fish analysis.xlsx'
        data = pd.DataFrame(pd.read_excel(path, sheet_name = 'Fish summary'))
        def convertRow(row):
            out = {
                'Fish name': row[0],
                'Average': round(row[1],2),
                'Min': round(row[2], 2),
                'Max': round(row[3], 2)}
            return out
        for i in data.iterrows():
            row = i[1]
            transformed_data = convertRow(row)
            result.append(transformed_data)
            if print_dict:
                print(transformed_data,',', sep = '')
        return result

        