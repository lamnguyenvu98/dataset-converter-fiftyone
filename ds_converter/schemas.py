from pydantic import BaseModel, field_validator
from typing import List, Optional, Any
import fiftyone.types as fot
import inspect

from .exception import DatasetTypeError

class DatasetImporter(BaseModel, extra="allow"):
    dataset_dir: Optional[str] = None
    dataset_type: str
    data_path: Optional[str] = None
    labels_path: Optional[str] = None
    label_field: Optional[Any] = None
    tags: Optional[str] = None
    expand_schema: bool = True
    dynamic: bool = False
    add_info: bool = True
    progress: Optional[Any] = None

    def __init__(self, **data):
        extra_args = data.pop('extra_args', {})
        super().__init__(**data)
        self.validate_extra_args(extra_args)
        for key, value in extra_args.items():
            if value == "":
                setattr(self, key, None)
            else:
                setattr(self, key, value)

    def validate_extra_args(self, extra_args):
        dataset: fot.Dataset = getattr(fot, self.dataset_type)()
        dataset_import = dataset.get_dataset_importer_cls()
        spec = inspect.getfullargspec(dataset_import)
        for k, v in extra_args.items():
            if k not in spec.args:
                raise TypeError(f"{k} is not argument for {dataset_import}. All parameters support are: {spec.args}.\n{dataset_import.__doc__}")

    @field_validator("*")
    def validate_empty_string(cls, value):
        if value == "":
            return None
        return value

    @field_validator('dataset_type')
    def check_dataset_type_fiftyone(cls, value):
        if not hasattr(fot, value):
            raise DatasetTypeError(f"{value} is not supported in fiftyone. Follow below link to see all dataset types: https://docs.voxel51.com/user_guide/dataset_creation/datasets.html#supported-formats")
        return value

class DatasetExporter(BaseModel, extra="allow"):
    export_dir: Optional[str] = None
    dataset_type: str
    data_path: Optional[str]
    labels_path: Optional[str]
    export_media: Optional[bool] = None
    label_field: Optional[Any] = None
    rel_dir: Optional[Any] = None
    frame_labels_field: Optional[Any] = None
    overwrite: bool = False
    progress: Optional[Any] = None
    tags: Optional[Any] = None

    def __init__(self, **data):
        extra_args = data.pop('extra_args', {})
        super().__init__(**data)

        self.validate_extra_args(extra_args)
        for key, value in extra_args.items():
            if value == "":
                setattr(self, key, None)
            else:
                setattr(self, key, value)

    def validate_extra_args(self, extra_args):
        dataset: fot.Dataset = getattr(fot, self.dataset_type)()
        dataset_export = dataset.get_dataset_exporter_cls()
        spec = inspect.getfullargspec(dataset_export)
        for k, v in extra_args.items():
            if k not in spec.args:
                raise TypeError(f"{k} is not argument for {dataset_export}. All parameters support are: {spec.args}.\n{dataset_export.__doc__}")

    @field_validator("*", mode="after")
    def validate_empty_string(cls, value):
        if value == "":
            return None
        return value

    @field_validator('dataset_type')
    def check_dataset_type_fiftyone(cls, value):
        if not hasattr(fot, value):
            raise DatasetTypeError(f"{value} is not supported in fiftyone. Follow below link to see all dataset types: https://docs.voxel51.com/user_guide/dataset_creation/datasets.html#supported-formats")
        return value

class Dataset(BaseModel):
    name_dataset: Optional[str] = None
    DatasetImport: List[DatasetImporter]
    DatasetExport: List[DatasetExporter]