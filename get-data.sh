#!/usr/bin/env bash

# Download latest Pedestrian traffic datasets and then prep for use in Dashboard

set -e

# directory to download data into
DATA_DIR=data

# https://data.melbourne.vic.gov.au/Transport/Pedestrian-Counting-System-2009-to-Present-counts-/b2ak-trbp
COUNT_DATASET_ID=b2ak-trbp

# https://data.melbourne.vic.gov.au/Transport/Pedestrian-Counting-System-Sensor-Locations/h57g-5234
SENSOR_DATASET_ID=h57g-5234


download_dataset () {
    wget --content-disposition --backups=3 --directory-prefix=${DATA_DIR} \
         https://data.melbourne.vic.gov.au/api/views/${1}/rows.csv?accessType=DOWNLOAD

}

download_dataset ${COUNT_DATASET_ID}
download_dataset ${SENSOR_DATASET_ID}

# prep data for use in Dashboard
echo "Making parquet file..."
python make_parquet.py
echo "Done."
