from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional, Any
import fiftyone.types as fot
import inspect

from ds_converter.exception import DatasetTypeError
from ds_converter.custom_loader import registry

class DatasetAddImportInfo(BaseModel):
    label_field: Optional[Any] = None
    tags: Optional[Any] = None
    expand_schema: bool = True
    dynamic: bool = False
    add_info: bool = True
    progress: Optional[Any] = None

class DatasetImporter(BaseModel):
    dataset_type: str
    importer_args: dict = Field(default_factory=dict)
    add_import_args: DatasetAddImportInfo

    @model_validator(mode='after')
    def validate_importer_args(self):
        importer_args = self.importer_args
        dataset_type_name = self.dataset_type
        if hasattr(fot, dataset_type_name):
            dataset: fot.Dataset = getattr(fot, dataset_type_name)()
            dataset_importer = dataset.get_dataset_importer_cls()
        elif dataset_type_name in registry:
            dataset_importer = registry.get(dataset_type_name)
        else:
            raise DatasetTypeError(f"{dataset_type_name} is not supported in fiftyone. Follow below link to see all dataset types: https://docs.voxel51.com/user_guide/dataset_creation/datasets.html#supported-formats")
        spec = inspect.getfullargspec(dataset_importer)
        for key in importer_args.keys():
            if key not in spec.args:
                raise TypeError(f"{key} in DatasetImport.importer_args is not argument for : {dataset_importer.__name__}. All parameters support are: {spec.args}.\n{dataset_importer.__doc__}")
        return self

    @field_validator('dataset_type', mode="before")
    @classmethod
    def check_dataset_type_fiftyone(cls, value):
        if not hasattr(fot, value) and value not in registry:
            raise DatasetTypeError(f"{value} is not supported in fiftyone. Follow below link to see all dataset types: https://docs.voxel51.com/user_guide/dataset_creation/datasets.html#supported-formats")
        return value

class DatasetExtraExportInfo(BaseModel):
    label_field: Optional[Any] = None
    frame_labels_field: Optional[Any] = None
    overwrite: bool = False
    progress: Optional[Any] = None

class DatasetExporter(BaseModel):
    dataset_type: str
    split: Optional[str] = None
    exporter_args: dict = Field(default_factory=dict)
    extra_export_args: DatasetExtraExportInfo

    @model_validator(mode="after")
    def validate_exporter_args(self):
        exporter_args = self.exporter_args
        dataset: fot.Dataset = getattr(fot, self.dataset_type)()
        dataset_export = dataset.get_dataset_exporter_cls()
        spec = inspect.getfullargspec(dataset_export)
        for key in exporter_args.keys():
            if key not in spec.args:
                raise TypeError(f"{key} in DatasetExport.exporter_args is not argument for {dataset_export.__name__}. All parameters support are: {spec.args}.\n{dataset_export.__doc__}")
        return self

    @field_validator('dataset_type')
    @classmethod
    def check_dataset_type_fiftyone(cls, value):
        if not hasattr(fot, value):
            raise DatasetTypeError(f"{value} is not supported in fiftyone. Follow below link to see all dataset types: https://docs.voxel51.com/user_guide/dataset_creation/datasets.html#supported-formats")
        return value

class Dataset(BaseModel):
    name: Optional[str] = None
    DatasetImport: List[DatasetImporter]
    DatasetExport: List[DatasetExporter]