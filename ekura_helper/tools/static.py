# Static variables
APP_NAME = 'Ekura helper'
APP_FOLDER_NAME = 'Ekura-helper'
GAME_WINDOW_NAME = 'Ekura(' # Used for window name lookup
LAUNCHER_WINDOW_NAME = 'Ekura Launcher'
LAUNCHER_APP_NAME = 'Ekura' # Used to find the launcher in the windows search


# Pytesseract variables (read more here https://pypi.org/project/pytesseract/)
# Tesseract-OCR installer at https://github.com/UB-Mannheim/tesseract/wiki
PYTESSERACT_PATH = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract' # 'tesseract' app in the Tesseract-OCR 
TESSDATA_DIR_CONFIG = r'--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"' # "tessdata" folder in the Tesseract-OCR

### GAME ###

# Game window coordinates
MESSAGE_LOG_COORD = [0.292, 0.880, 0.708, 0.953] # Message log range
CHAR_POS_COORD = [0.936, 0.209, 0.979, 0.230] # Character position
VALIDATION_COORDS = [CHAR_POS_COORD, MESSAGE_LOG_COORD] # Used in game position validation

### MINING ###

# Pixel colors
NODE_PIXELS = [[46, 115, 61], [65, 162, 85], [89, 220, 116], [89, 222, 117], [84, 208, 110], [70, 173, 91], [72, 180, 95]] # Node - green

# Regex patterns
CHAR_POS_REGEX = r'\(\d+,\ ?\d+\)'
CHAR_POS_REGEX_EXTRACT = r'\((.*),\ ?(.*)\)'

# Word lists
MINING_DONE_KEYWORDS = ['Tvá', 'zkušenost', 'tímto', 'krumpáčem', 'potřebných', 'bodů', 'Pauzička', 'Takhle', 'říši', 'nevybudujeme']
MINING_IMPOSSIBLE_KEYWORDS = ['Tady', 'kopat', 'nemůžeš', 'žádná', 'nenachází']

### FISHING ###

FISHING_LURE_SLOT = '1' # Slot in the hotbar with the lure

FISHING_IMPOSSIBLE_KEYWORDS = ['Tady', 'nemůžeš', 'lovit', 'ryby']
FISHING_NO_LURE_KEYWORDS = ['žádnou', 'Pokud', 'chceš', 'chytat', 'ryby', 'musíš', 'použít', 'návnadu']
FISHING_LURE_ON_KEYWORDS = ['Na', 'háčku', 'se', 'houpe']
FISHING_FISH_ON_KEYWORDS = ['Vypadá', 'to', 'že', 'právě', 'zabírá', 'na']
FISHING_FISH_GONE_KEYWORDS = ['A', 'úlovek', 'fuč']
FISHING_FISH_CAUGHT_KEYWORDS = ['Tvým', 'úlovkem', 'délce']

# Fish names, and the time required to wait for a successful catch
FISHING_FISH_INFORMATION = [
    {'Fish name': 'Pstruh říční', 'Average': 1.0, 'Min': 1.0, 'Max': 1.0},
    {'Fish name': 'Koruška', 'Average': 0.0, 'Min': 0.0, 'Max': 0.0},
    {'Fish name': 'Candát', 'Average': 2.05, 'Min': 0.76, 'Max': 4.35},
    {'Fish name': 'Mandarínová ryba', 'Average': 1.6, 'Min': 0.77, 'Max': 2.41},
    {'Fish name': 'Kapr', 'Average': 1.72, 'Min': 0.88, 'Max': 3.29},
    {'Fish name': 'Losos', 'Average': 1.8, 'Min': 0.57, 'Max': 3.75},
    {'Fish name': 'Amur bílý', 'Average': 1.4, 'Min': 0.97, 'Max': 2.2},
    {'Fish name': 'Pstruh', 'Average': 2.05, 'Min': 1.17, 'Max': 3.06},
    {'Fish name': 'Úhoř', 'Average': 2.12, 'Min': 1.26, 'Max': 3.5},
    {'Fish name': 'Pstruh duhový', 'Average': 1.44, 'Min': 1.09, 'Max': 1.9},
    {'Fish name': 'Perlín ostrobřichý', 'Average': 1.88, 'Min': 1.23, 'Max': 2.55},
    {'Fish name': 'Okoun', 'Average': 2.02, 'Min': 1.93, 'Max': 2.07},
    {'Fish name': 'Tenchi', 'Average': 1.23, 'Min': 1.09, 'Max': 1.36},
    {'Fish name': 'Sumec', 'Average': 0.0, 'Min': 0.0, 'Max': 0.0},
    {'Fish name': 'Mřenka', 'Average': 2.95, 'Min': 2.95, 'Max': 2.95},
    {'Fish name': 'Lotosová ryba', 'Average': 1.38, 'Min': 1.17, 'Max': 1.71},
    {'Fish name': 'Ayu', 'Average': 3.11, 'Min': 3.11, 'Max': 3.11},
    {'Fish name': 'Shiri', 'Average': 1.47, 'Min': 1.47, 'Max': 1.47},
    {'Fish name': 'Stříbrný klíč', 'Average': 2.12, 'Min': 1.37, 'Max': 2.54},
    {'Fish name': 'Zlatý klíč', 'Average': 0.0, 'Min': 0.0, 'Max': 0.0},
    {'Fish name': 'Kámen duše', 'Average': 1.01, 'Min': 0.89, 'Max': 1.12},
    {'Fish name': 'Požehnaný pergamen', 'Average': 1.71, 'Min': 1.71, 'Max': 1.71},
    {'Fish name': 'Malá ryba', 'Average': 2.13, 'Min': 0.65, 'Max': 4.04},
    {'Fish name': 'Velký candát', 'Average': 3.63, 'Min': 2.39, 'Max': 4.38},
    {'Fish name': 'Kapr hladký', 'Average': 0.0, 'Min': 0.0, 'Max': 0.0},
    {'Fish name': 'Zlatá rybka', 'Average': 2.71, 'Min': 2.71, 'Max': 2.71},
    {'Fish name': 'Prut zlata (1kk)', 'Average': 0.0, 'Min': 0.0, 'Max': 0.0},
]

FISHING_BOT_TYPOS = {
    'Mandarinová ryba': 'Mandarínová ryba',
    'Mřénka': 'Mřenka',
    'Lolosová ryba': 'Lotosová ryba',
}

### VARIOUS ###

# Game launcher window coordinates
LAUNCHER_NAME_COORD = [0.460, 0.698, 0.606, 0.745] # For text reading
LAUNCHER_NAME_POS = [0.530, 0.715] # For clicking 
LAUNCHER_PW_POS = [0.530, 0.785]
LAUNCHER_START_POS = [0.530, 0.860]

# Monitor coordinates
MONITOR_LAUNCHER_DEFAULT_COORD = [0.233, 0.245, 0.660, 0.616] # Default coordinates of the launcher, in terms of monitor size


### KEYS ###
KEYS = {
    '1':0x02,
    '2':0x03,
    '3':0x04,
    '4':0x05,
    '5':0x06,
    '6':0x07,
    '7':0x08,
    '8':0x09,
    '9':0x0A,
    'F1':0x3B,
    'F2':0x3C,
    'F3':0x3D,
    'F4':0x3E,
    'A':0x1E,
    'C':0x2E,
    'D':0x20,
    'I':0x17,
    'K':0x25,
    'M':0x32,
    'S':0x1F,
    'W':0x11,
    'Z':0x2C,
    'SPACE':0x39,
}