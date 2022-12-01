APP_NAME = 'Ekura miner'

# Static variables

# Pytesseract variables (read more here https://pypi.org/project/pytesseract/)
# Tesseract-OCR installer at https://github.com/UB-Mannheim/tesseract/wiki
PYTESSERACT_PATH = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract' # 'tesseract' app in the Tesseract-OCR 
TESSDATA_DIR_CONFIG = r'--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"' # "tessdata" folder in the Tesseract-OCR

### MINING PROCESS ###

# Pixel colors
NODE_PIXELS = [[89, 220, 116], [70, 173, 91], [72, 180, 95]] # Node - green

# Regex patterns
COORD_REGEX = r'\(\d+,\ \d+\)'
COORD_REGEX_EXTRACT = r'\((.*),\ (.*)\)'

# Coordinates
CHAR_POS_COORD = [0.936, 0.207, 0.974, 0.227] # Character position
MINING_TEXT_COORD = [0.292, 0.818, 0.708, 0.919] # Message log range

# Word lists
MINING_DONE_KEYWORDS = ['Tvá', 'zkušenost', 'tímto', 'krumpáčem', 'potřebných', 'bodů', 'Pauzička', 'Takhle', 'říši', 'nevybudujeme']
MINING_IMPOSSIBLE_KEYWORDS = ['Tady', 'kopat', 'nemůžeš', 'žádná', 'nenachází']

