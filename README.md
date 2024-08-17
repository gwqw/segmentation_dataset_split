# Segmentation dataset splitter

Segmentation dataset splitter splits dataset on parts, e.g. train/val/test.

## How to use

Create config file, default is `split_dataset_on_train_val.yaml`, but you set any config by `-c` option.
```
input_image_path -- path to images
input_annotation_path -- path to annotation (segmentation)
image_template, annotation_template -- optional fields, can be used, if filenames of annotations != filenames of segmentations. 
	So they will be matched by regex.groups, groups must contain same info for the image and the corresponding segmentation. 
	By default original filenames will be used.
part_names -- names of parts, e.g. train, val, test
part_sizes -- part sizes (len(part_sizes) must be == len(images)). Can be in % or in parts on 1.
output_image_path -- output path for splits, image will be saved in output_image_path/split_name directory for each split
output_annotation_path -- output annotation path
rename_annotations -- optional, can be used if name of annotation != name of image.
	So annotations will be renamed and will have same names like corresponding images, but they will have their original extensions. 
	By default = False
to_shuffle -- shuffle dataset before split, default=True
```

run splitter:
```
python3 split_dataset_on_train_val.py 
```
or
```
python3 split_dataset_on_train_val.py -c config_name.yaml
```