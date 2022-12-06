# Static variables
APP_NAME = 'Ekura miner'
GAME_WINDOW_NAME = 'Ekura(' # Used for window name lookup
LAUNCHER_WINDOW_NAME = 'Ekura Launcher'
LAUNCHER_APP_NAME = 'Ekura' # Used to find the launcher in the windows search


# Pytesseract variables (read more here https://pypi.org/project/pytesseract/)
# Tesseract-OCR installer at https://github.com/UB-Mannheim/tesseract/wiki
PYTESSERACT_PATH = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract' # 'tesseract' app in the Tesseract-OCR 
TESSDATA_DIR_CONFIG = r'--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"' # "tessdata" folder in the Tesseract-OCR

### KEYS ###
KEYS = {
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

### MINING PROCESS ###

# Pixel colors
NODE_PIXELS = [[46, 115, 61], [65, 162, 85], [89, 220, 116], [89, 222, 117], [84, 208, 110], [70, 173, 91], [72, 180, 95]] # Node - green

# Regex patterns
CHAR_POS_REGEX = r'\(\d+,\ ?\d+\)'
CHAR_POS_REGEX_EXTRACT = r'\((.*),\ ?(.*)\)'

# Game window coordinates
CHAR_POS_COORD = [0.936, 0.209, 0.979, 0.230] # Character position
MINING_TEXT_COORD = [0.292, 0.800, 0.708, 0.953] # Message log range
VALIDATION_COORDS = [CHAR_POS_COORD, MINING_TEXT_COORD] # Used in game position validation

# Game launcher window coordinates
LAUNCHER_NAME_COORD = [0.530, 0.715]
LAUNCHER_PW_COORD = [0.530, 0.785]
LAUNCHER_START_COORD = [0.530, 0.860]

# Monitor coordinates



# Word lists
MINING_DONE_KEYWORDS = ['Tvá', 'zkušenost', 'tímto', 'krumpáčem', 'potřebných', 'bodů', 'Pauzička', 'Takhle', 'říši', 'nevybudujeme']
MINING_IMPOSSIBLE_KEYWORDS = ['Tady', 'kopat', 'nemůžeš', 'žádná', 'nenachází']


### MOVE TO LOCAL_SETTINGS.PY LATER ###
MINER_CHAR_NAME = 'Gintaro'

