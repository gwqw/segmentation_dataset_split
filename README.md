# Image dataset splitter

Image (segmentation) dataset splitter splits dataset on parts, e.g. train/val/test. It assumes that annotation (gt) for each input image is separate file.

## How to use

Create config file, default is `split_dataset_on_train_val.yaml`, but you can pass any config by `-c` option.

Simple config:
```
input_image_path		path to images to split
input_annotation_path	path to annotations to split
part_names				names of parts, e.g. train, val, test
part_sizes				part sizes (len(part_sizes) must be == len(images)). Can be in % or in parts on 1.
output_image_path		output path for splits, image will be saved in output_image_path/split_name directory for each split. Or if output_image_path contains "{split}" string, it will be replaced bey split name.
output_annotation_path	output annotation path (same rules as in output_image_path)
to_shuffle				shuffle dataset before split, default=True
split_file_description	if set, script will save split info: image and annotation filenames separated with ' ' to this filename. "{split}" must be in this filename.
```

Additional config fields for matching image - gt, if image and annotation have different filenames:
```
image_template, annotation_template -- optional fields, can be used, if filenames of annotations != filenames of images.
	So they will be matched by regex.groups, groups must contain same info for the image and the corresponding annotation.
	By default original filenames will be used.
rename_annotations -- optional, can be used if name of annotation != name of image.
	So annotations will be renamed and will have same names like corresponding images, but they will have their original extensions.
	By default = False
```

run splitter:
```
python3 split_dataset_on_train_val.py
```
or
```
python3 split_dataset_on_train_val.py -c config_name.yaml
```
