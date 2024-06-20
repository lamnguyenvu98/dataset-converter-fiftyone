import os

import eta.core.utils as etau

import fiftyone as fo
from fiftyone.utils.voc import VOCDetectionDatasetImporter
import fiftyone.core.storage as fos

registry = {}

class CustomVOCImporter(VOCDetectionDatasetImporter):
    def __init__(self, split_file: str, dataset_dir=None, data_path=None, labels_path=None, include_all_data=False, extra_attrs=True, shuffle=False, seed=None, max_samples=None):
        super().__init__(dataset_dir, data_path, labels_path, include_all_data, extra_attrs, shuffle, seed, max_samples)
        self.split_file = split_file
    
    def setup(self):
        splits = self.read_split_file(self.split_file)
        
        image_paths_map = self._load_data_map(
            self.data_path, ignore_exts=True, recursive=True
        )
        
        image_paths_map = {k: v for k, v in image_paths_map.items() if k in splits}

        if self.labels_path is not None and os.path.isdir(self.labels_path):
            labels_path = fos.normpath(self.labels_path)
            labels_paths_map = {
                os.path.splitext(p)[0]: os.path.join(labels_path, p)
                for p in etau.list_files(labels_path, recursive=True)
                if etau.has_extension(p, ".xml")
            }
            labels_paths_map = {k: v for k, v in labels_paths_map.items() if k in splits}
        else:
            labels_paths_map = {}

        uuids = set(labels_paths_map.keys())

        if self.include_all_data:
            uuids.update(image_paths_map.keys())

        uuids = self._preprocess_list(sorted(uuids))

        self._image_paths_map = image_paths_map
        self._labels_paths_map = labels_paths_map
        self._uuids = uuids
        self._num_samples = len(uuids)
    
    def read_split_file(self, file):
        with open(file, 'r') as f:
            splits = f.readlines()
            splits = [split.strip('\n') for split in splits]
        
        return splits

registry.update({CustomVOCImporter.__name__: CustomVOCImporter})