import fiftyone as fo
import fiftyone.types as fot
from fiftyone.utils.voc import VOCDetectionDatasetImporter

from .config import load_config
from .schemas import Dataset

dataset = fo.Dataset(
    name="coco-yolo-val"
)

config = load_config('config/voc2yolo.toml')

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

dataset = build_dataset(config)
# print(dataset)
# session = fo.launch_app(dataset=dataset)
# session.wait(-1)