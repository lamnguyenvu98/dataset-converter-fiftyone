from .registry_dataset import Registry

import os
import importlib

# Automatically import all Python files in the datasets directory
dataset_dir = os.path.dirname(__file__)
for filename in os.listdir(dataset_dir):
    if filename.endswith('.py') and not filename.startswith('__') and not filename.startswith('registry_dataset'):
        module_name = os.path.splitext(filename)[0]
        importlib.import_module(f'ds_converter.datasets.{module_name}')