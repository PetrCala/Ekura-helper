import gzip, pickle

def writeLocalData(data, path:str = None):
    '''Input an object and rewrite the local data file with this object.
    Return None.
    '''
    data_path = 'ekura_helper/tools/localdata.py' if path is None else path
    with gzip.open(data_path, 'wb') as f:
        pickle.dump(data, f)
    return None

def readLocalData(path:str = None):
    '''Read the local data file and return its contents.
    '''
    data_path = 'ekura_helper/tools/localdata.py' if path is None else path
    with gzip.open(data_path, 'rb') as f:
        data = pickle.load(f)
    return data




    
