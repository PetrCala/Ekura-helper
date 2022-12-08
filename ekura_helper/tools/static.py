# Static variables
APP_NAME = 'Ekura miner'
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
FISHING_FISH_ON_KEYWORDS = ['Vypadá', 'to', 'že', 'právě', 'zabírá', 'na']
FISHING_FISH_GONE_KEYWORDS = ['A', 'úlovek', 'fuč']
FISHING_FISH_CAUGHT_KEYWORDS = ['Tvým', 'úlovkem', 'délce']

# Fish names, and the time required to wait for a successful catch
FISHING_0S_FISH = ['Pstruh říční', 'Koruška', 'Nožík']
FISHING_3S_FISH = ['Candát', 'Mandarínová ryba', 'Mandarinová ryba', 'Kapr', 'Losos', 'Amur bílý', 'Pstruh', 'Úhoř', 'Pstruh duhový', 'Perlín ostrobřichý',
    'Okoun', 'Tenchi', 'Sumec', 'Mřenka', 'Mřénka', 'Lotosová ryba', 'Lolosová ryba', 'Ayu', 'Shiri', 'Stříbrný klíč', 'Zlatý klíč', 'Kámen duše',
    'Požehnaný pergamen', 'Malá ryba']
FISHING_5S_FISH = ['Velký candát', 'Kapr hladký', 'Zlatá rybka', 'Prut zlata (1kk)']
FISHING_ALL_FISH = [FISHING_0S_FISH, FISHING_3S_FISH, FISHING_5S_FISH]

# Fish wait time information
FISHING_FISH_INFORMATION = [
    {'Fish names': FISHING_0S_FISH, 'Time': 2},
    {'Fish names': FISHING_3S_FISH, 'Time': 2.5},
    {'Fish names': FISHING_5S_FISH, 'Time': 4.5}
]


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