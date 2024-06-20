import fiftyone as fo
import fiftyone.types as fot
from fiftyone.core.view import DatasetView
import argparse

from .config import load_config
from .schemas import Dataset

def build_dataset(config: Dataset):
    dataset = fo.Dataset(name=config.name_dataset)
    dataset.tags = []
    for args in config.DatasetImport:
        dataset_type = getattr(fot, args.dataset_type)
        dataset.add_dir(
            dataset_type=dataset_type,
            **args.model_dump(exclude="dataset_type")
        )
        if args.tags is not None:
            dataset.tags.append(args.tags)
    
    return dataset

def export_dataset(dataset, config: Dataset):
    for args in config.DatasetExport:
        dataset_type = getattr(fot, args.dataset_type)
        view: DatasetView = dataset.match_tags(args.tags)
        excluded = ['dataset_type', 'tags']
        if hasattr(args, 'classes'):
            if args.classes == 'default':
                args.classes = dataset.default_classes
        view.export(
            dataset_type=dataset_type,
            **args.model_dump(exclude=excluded)
        )

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config-file", 
        "-c", 
        type=str, 
        required=True,
        help="Config file (.toml)"
    )
    args = parser.parse_args()
    config = load_config(args.config_file)
    
    dataset = build_dataset(config)
    print("\nDataset info: \n", dataset, "\n")
    export_dataset(dataset, config)

if __name__ == '__main__':
    run()