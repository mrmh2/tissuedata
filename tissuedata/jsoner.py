"""tissuedata analysis."""

import os
import json
import logging
import argparse

import numpy as np

from jicbioimage.core.image import Image
from jicbioimage.core.transform import transformation
from jicbioimage.core.io import AutoName, AutoWrite

__version__ = "0.0.1"

AutoName.prefix_format = "{:03d}_"


class Cell(dict):
    @classmethod
    def from_point_arrays(cls, point_arrays):
        return cell_data_from_point_arrays(point_arrays)


@transformation
def identity(image):
    """Return the image as is."""
    return image


def analyse_file(fpath, output_directory):
    """Analyse a single file."""
    logging.info("Analysing file: {}".format(fpath))
    image = Image.from_file(fpath)
    image = identity(image)


def analyse_directory(input_directory, output_directory):
    """Analyse all the files in a directory."""
    logging.info("Analysing files in directory: {}".format(input_directory))
    for fname in os.listdir(input_directory):
        fpath = os.path.join(input_directory, fname)
        analyse_file(fpath, output_directory)


def convert_rgb_array_to_uint32(segmented_image):
    """Return 2D uint32 array of identifiers, converting from the input image
    as a MxNx3 RGB array."""

    image_u32 = segmented_image.astype(np.uint32)

    R = image_u32[:, :, 0]
    G = image_u32[:, :, 1]
    B = image_u32[:, :, 2]

    identifier_image = B + (G << 8) + (R << 16)

    return identifier_image


def cell_data_from_point_arrays(point_arrays):
    float_centroid = map(np.mean, point_arrays)
    int_centroid = map(int, float_centroid)

    top_left = map(np.min, point_arrays)

    pixel_area = len(point_arrays[0])

    return {"top_left": top_left, "centroid": int_centroid, "pixel_area": pixel_area}


def parse_metadata_file(input_metadata_filename):
    """Return dictionary of metadata in filename, which should be in the format:

    [Heading]
    key1 = value1
    key2 = value2
    """

    with open(input_metadata_filename) as f:
        raw_lines = f.readlines()

    stripped_lines = [l.strip() for l in raw_lines]
    # Skip first line (heading) and last line (blank)
    split_lines = [l.split(' = ') for l in stripped_lines[1:-1]]

    return dict(split_lines)


def cell_dict_from_identifier_image(identifier_image):
    """Return a dictionary in the form:

    identifier : properties

    where identifier is the identifier of the cell, and properties are
    key value pairs derived from that cell."""

    all_identifiers = np.unique(identifier_image)

    cell_dict = {}
    for id in all_identifiers:
        if id != 0:
            cell = Cell.from_point_arrays(np.where(identifier_image == id))
            cell_dict[str(id)] = cell

    return cell_dict


def extract_common_metadata(input_metadata_filename):
    """Return a dictionary of the metadata extracted from the input file that
    is common to all cells in the file."""

    metadata = parse_metadata_file(input_metadata_filename)
    vx = metadata['voxel size x']
    vy = metadata['voxel size y']

    common_metadata = {"vx": vx, "vy": vy}

    return common_metadata


def extract_has_data(input_has_filename):
    with open(input_has_filename) as f:
        raw_lines = f.readlines()

    has = raw_lines[0].strip()

    return {"has": float(has)}


def read_image_and_output_json(input_segmentation_filename,
                               input_metadata_filename,
                               input_has_filename):
    common_metadata = extract_common_metadata(input_metadata_filename)
    has_data = extract_has_data(input_has_filename)
    common_metadata.update(has_data)
    segmented_image = Image.from_file(input_segmentation_filename)
    identifier_image = convert_rgb_array_to_uint32(segmented_image)

    all_identifiers = np.unique(identifier_image)

    cell_dict = cell_dict_from_identifier_image(identifier_image)

    for cell in cell_dict.values():
        cell.update(common_metadata)

    all_cells = {"cells": cell_dict}

    print json.dumps(all_cells, indent=2)


def main():
    # Parse the command line arguments.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_segmentation", help="Input segmentation file.")
    parser.add_argument("input_metadata", help="Input microscope metadata.")
    parser.add_argument("input_has_file", help="File containing HAS data.")
    args = parser.parse_args()

    read_image_and_output_json(args.input_segmentation, args.input_metadata,
                               args.input_has_file)

    # Create the output directory if it does not exist.
    # if not os.path.isdir(args.output_dir):
    #     os.mkdir(args.output_dir)
    # AutoName.directory = args.output_dir

    # Setup a logger for the script.
    # log_fname = "audit.log"
    # log_fpath = os.path.join(args.output_dir, log_fname)
    # logging_level = logging.INFO
    # if args.debug:
    #     logging_level = logging.DEBUG
    # logging.basicConfig(filename=log_fpath, level=logging_level)

    # # Log some basic information about the script that is running.
    # logging.info("Script name: {}".format(__file__))
    # logging.info("Script version: {}".format(__version__))


if __name__ == "__main__":
    main()
