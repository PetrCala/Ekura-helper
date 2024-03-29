﻿import os
import sys
import gzip, pickle
from pathlib import Path

def validateLocalDataExistence():
    '''Check for the existence of the local data file. If it is missing,
    create the file, with an empty dictionary inside.
    '''
    path = str(Path().absolute()) + r'\localdata.py'
    if not Path(path).is_file():
        dummy_data = {'ACCOUNT_LIST': [''], 'CHARACTER_LIST': ['']}
        with gzip.open(path, 'wb') as f:
            pickle.dump(dummy_data, f)
    return None

def writeLocalData(data, path:str = None):
    '''Input an object and rewrite the local data file with this object.
    Return None.
    '''
    if path is None:
        path = str(Path().absolute()) + r'\localdata.py'
    with gzip.open(path, 'wb') as f:
        pickle.dump(data, f)
    return None

def readLocalData(path:str = None):
    '''Read the local data file and return its contents.
    '''
    if path is None:
        path = str(Path().absolute()) + r'\localdata.py'
    with gzip.open(path, 'rb') as f:
        data = pickle.load(f)
    return data

def modifyLocalData(key:str, value):
    '''Define a key, and a value of the data dictionary, which to modify,
    open the local data file, and adjust it accordingly. Return None.

    Args:
        key (str): Key of the data part to change.
        value (_type_): Value which should correspond to said key.
    '''
    local_data = readLocalData()
    local_data[key] = value
    writeLocalData(local_data)
    return None

def getTesseractPath(file = 'exe'):
    '''Make the pytesseract launcher path user specific.
    :arg:
        file (str) - Type of file to fetch. If None, fetch the pytesseract
            directory. If 'exe', fetch the executable. If 'conf', fetch
            the configuration file. Defaults to 'exe'.
    '''
    if not file in (None, 'exe', 'conf'):
        raise ValueError(f'{file} must be one of the following - None, \'exe\', or \'conf\'.')
    base_path = r'C:\\Program Files (x86)\\Tesseract-OCR'
    if not Path(base_path).is_dir():
        raise SystemError('Tesseract not installed')
    if file == 'exe':
        return base_path + r'\\tesseract'
    elif file == 'conf':
        return r'--tessdata-dir "' + base_path + r'\\tessdata"'
    return base_path
