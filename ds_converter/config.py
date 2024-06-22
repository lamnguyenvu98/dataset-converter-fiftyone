import toml

from ds_converter.schemas import Dataset

def load_config(path):
    with open(path, 'r') as f:
        config = toml.load(f)
    return Dataset(**config)

if __name__ == '__main__':
    print(load_config('config/config.toml'))