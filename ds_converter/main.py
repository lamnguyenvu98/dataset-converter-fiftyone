import fiftyone as fo
import fiftyone.types as fot
from fiftyone.core.view import DatasetView
import argparse

from ds_converter.config import load_config
from ds_converter.schemas import Dataset
from ds_converter.datasets.registry_dataset import Registry
from ds_converter.exception import DatasetTypeError

def build_dataset_import(dataset_type: str, **kwargs):
    if hasattr(fot, dataset_type):
        dataset: fot.Dataset = getattr(fot, dataset_type)()
        dataset_importer = dataset.get_dataset_importer_cls()
    else:
        dataset_importer = Registry.get_instance(
            type='importer',
            dataset_type=dataset_type
        )
    return dataset_importer(**kwargs)

def build_dataset_export(dataset_type: str, **kwargs):
    if hasattr(fot, dataset_type):
        dataset: fot.Dataset = getattr(fot, dataset_type)()
        dataset_exporter = dataset.get_dataset_exporter_cls()
    else:
        dataset_exporter = Registry.get_instance(
            type='exporter',
            dataset_type=dataset_type
        )
    return dataset_exporter(**kwargs)


def build_dataset(config: Dataset):
    dataset = fo.Dataset(name=config.name)
    dataset.tags = []
    for args in config.DatasetImport:
        dataset_importer = build_dataset_import(
            dataset_type=args.dataset_type,
            **args.importer_args
        )
        
        dataset.add_importer(
            dataset_importer=dataset_importer,
            **args.add_import_args.model_dump()
        )
    
    return dataset

def export_dataset(dataset: fo.Dataset, config: Dataset):
    for args in config.DatasetExport:
        view: DatasetView = dataset.match_tags(args.match_tags)
        classes = args.exporter_args.get('classes', None)
        if classes is None:
            classes = dataset.distinct("ground_truth.detections.label")
        elif classes == 'default':
            if len(dataset.default_classes) == 0:
                classes = dataset.distinct("ground_truth.detections.label")
            else:
                classes = dataset.default_classes
        args.exporter_args.update({'classes': classes})
        dataset_exporter = build_dataset_export(
            args.dataset_type,
            **args.exporter_args
        )
        view.export(
            dataset_exporter=dataset_exporter,
            **args.extra_export_args.model_dump()
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