# Create virtual environment, handle base path, create link to main.pyw, create localdata.py
import gzip, pickle
from pathlib import Path

base_path =  str(Path().absolute())
local_data_path = 'ekura_helper/tools/localdata.py'

# Create a file with an empty dict for the local data storage
if not Path(local_data_path).is_file():
    local_data_temp = {}
    with gzip.open(local_data_path, 'wb') as f:
        pickle.dump(local_data_temp, f)


