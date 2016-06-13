#!/usr/bin/env bash
# script for scraping data from existing data directory structures

# set -ex # debug

cd /Users/carterr/Dropbox/Postdoc_stuff/tissuedata/tissuedata/

data_path=$1
output_directory=$2

if [[ $# != 2 ]]; then
    echo "Usage: $0 [input_data_directory] [output_data_directory]"
    exit 4
fi

if [ ! -d "${output_directory}" ]; then
    mkdir ${output_directory}
fi

image_path=${data_path}/segmented_corrected

for image in "${image_path}"/*
do
    time_point=$(basename ${image} | cut -f 1 -d '.')
    echo Scraping data from from timepoint: ${time_point}
    metadata_path=${data_path}/microscope_metadata/${time_point}.txt
    has_path=${data_path}/has/${time_point}.txt
    output_path=${output_directory}/${time_point}.json

    python jsoner.py ${image} ${metadata_path} ${has_path} > ${output_path}
done