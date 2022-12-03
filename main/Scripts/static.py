APP_NAME = 'Ekura miner'

# Static variables

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

# Coordinates
CHAR_POS_COORD = [0.936, 0.209, 0.979, 0.230] # Character position
MINING_TEXT_COORD = [0.292, 0.818, 0.708, 0.919] # Message log range

# Word lists
MINING_DONE_KEYWORDS = ['Tvá', 'zkušenost', 'tímto', 'krumpáčem', 'potřebných', 'bodů', 'Pauzička', 'Takhle', 'říši', 'nevybudujeme']
MINING_IMPOSSIBLE_KEYWORDS = ['Tady', 'kopat', 'nemůžeš', 'žádná', 'nenachází']

