#!/usr/bin/env bash

DATA_DIR=${DATA_PATH-data}

mkdir -p ${DATA_DIR}
wget https://data.melbourne.vic.gov.au/api/views/b2ak-trbp/rows.csv?accessType=DOWNLOAD -O ${DATA_DIR}/Pedestrian_Counting_System___2009_to_Present__counts_per_hour_.csv
wget https://data.melbourne.vic.gov.au/api/views/h57g-5234/rows.csv?accessType=DOWNLOAD -O ${DATA_DIR}/Pedestrian_Counting_System_-_Sensor_Locations.csv
