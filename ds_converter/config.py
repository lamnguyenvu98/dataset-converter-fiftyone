import toml

from .schemas import Dataset

def load_config(path):
    with open(path, 'r') as f:
        config = toml.load(f)
    
    return Dataset(**config)