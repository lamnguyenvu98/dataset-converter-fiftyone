from ds_converter.datasets.custom_loader import CustomVOCImporter
import fiftyone as fo
import fiftyone.types as fot
from fiftyone.utils.yolo import YOLOv5DatasetExporter
from fiftyone.core.view import DatasetView

dataset = fo.Dataset(name="voc")

for mode in ['train']:
    importer = CustomVOCImporter(
        dataset_dir = '/home/pep/Datasets/VOCdevkit/VOC2012/',
        data_path = 'JPEGImages',
        labels_path = 'Annotations',
        split_file=f"/home/pep/Datasets/VOCdevkit/VOC2012/ImageSets/Main/{mode}.txt",
        # max_samples=300
    )

    dataset.add_importer(
        dataset_importer=importer,
        tags=f"{mode}"
    )

print(dataset)
print(dataset.default_classes)
print(dataset.distinct("ground_truth.detections.label"))

for mode in ['train', 'val']:
    view = dataset.match_tags(mode)
    exporter = YOLOv5DatasetExporter(
        export_dir = '/home/pep/Datasets/Coco2017/voc-yolo-test',
        export_media = True,
        split=mode,
        classes=dataset.distinct("ground_truth.detections.label")
    )

    view.export(
        dataset_exporter=exporter
    )