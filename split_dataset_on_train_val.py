import argparse
import os
import random
import re
import shutil
import typing as tp

import yaml

EPS = 1e-16


def _validate_config(config: tp.Dict[str, tp.Any]):
    assert "input_image_path" in config
    assert "input_annotation_path" in config
    assert "part_names" in config
    assert "part_sizes" in config
    assert "output_image_path" in config
    assert "output_annotation_path" in config
    assert len(config["part_names"]) == len(config["part_sizes"])


def _parse_config(config_filename: str) -> tp.Dict[str, tp.Any]:
    with open(config_filename) as f:
        cfg = yaml.safe_load(f)
        _validate_config(cfg)
        return cfg


def get_dataset_filenames(path: str, template: tp.Optional[str] = None) -> tp.Dict[str, str]:
    """
    get_dataset_filenames return dictionary key_from_filename -> filename
    key_from_filename = join all regex.goups with '_'
    (it's useful if annotation and image names are different)
    """
    filenames = {}
    if template is not None:
        re_template = re.compile(template)
    for entry in os.scandir(path=path):
        if not entry.is_file():
            continue
        filename = entry.name
        if template is not None:
            match = re_template.match(filename)
            if match is None:
                continue
            key = "_".join(match.groups())
            filenames[key] = filename
        else:
            filenames[filename] = filename
    return filenames


def _check_template(image_names: tp.Iterable[str], annotation_names: tp.Iterable[str]):
    """
    _check_template checks that for image names and annotation names are matched
    """
    image_names = sorted(image_names)
    annotation_names = sorted(annotation_names)
    for image_name, ann_name in zip(image_names, annotation_names):
        if image_name != ann_name:
            raise RuntimeError(f"image names != annotation_names: {image_name} != {ann_name}")


def _normalize(a: tp.List[float], target_sum: int) -> tp.List[int]:
    s = sum(a)
    return [int(target_sum * v / s) for v in a]


def split_names(names: tp.Iterable[str], part_names: tp.List[str], part_sizes: tp.List[float],
                to_shuffle: bool = True) -> tp.Dict[str, tp.List[str]]:
    """
    split_names splits dataset record names on train/val/test parts
    """
    part_sizes = _normalize(part_sizes, len(names))
    keys = list(names)
    if to_shuffle:
        random.shuffle(keys)
    else:
        keys.sort()
    parts: tp.Dict[str, tp.List[str]] = {}
    cur_idx = 0
    for part_name, part_size in zip(part_names, part_sizes):
        parts[part_name] = keys[cur_idx:cur_idx + part_size]
        cur_idx += part_size
    return parts


def _make_output_filename(input_filename: str, output_filename: str) -> str:
    """
    _make_output_filename renames filename, but preserves extension
    """
    _, i_ext = os.path.splitext(input_filename)
    o_name, _ = os.path.splitext(output_filename)
    return o_name + i_ext


def copy_files(input_path: str, file_names: tp.Dict[str, str], split: tp.Dict[str, tp.List[str]],
               output_path: str, output_filenames: tp.Optional[tp.Dict[str, str]] = None):
    """
    copy_files copies files to their split target positions
    """
    for split_name, split_keys in split.items():
        target_path = os.path.join(output_path, split_name)
        os.makedirs(target_path, exist_ok=True)
        for k in split_keys:
            input_filename = file_names[k]
            output_filename = _make_output_filename(input_filename, output_filenames[k])\
                if output_filenames else input_filename
            shutil.copy(os.path.join(input_path, input_filename), os.path.join(target_path, output_filename))


def main():
    parser = argparse.ArgumentParser(description="splits dataset on train/val/test parts")
    parser.add_argument("-c", "--config_name", default="split_dataset_on_train_val.yaml",
                        help="config file for splitter")
    args = parser.parse_args()
    cfg = _parse_config(args.config_name)
    image_names = get_dataset_filenames(cfg["input_image_path"], cfg.get("image_template"))
    annotation_names = get_dataset_filenames(cfg["input_annotation_path"], cfg.get("annotation_template"))
    _check_template(image_names.keys(), annotation_names.keys())
    split = split_names(image_names.keys(), cfg['part_names'], cfg['part_sizes'],
                        to_shuffle=cfg.get('to_shuffle', True))
    copy_files(cfg["input_image_path"], image_names, split, cfg['output_image_path'])
    new_ann_names = image_names if cfg.get("rename_annotations") else None
    copy_files(cfg["input_annotation_path"], annotation_names, split, cfg['output_annotation_path'], new_ann_names)


if __name__ == "__main__":
    main()
