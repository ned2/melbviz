#!/usr/bin/env python

from melbviz.pedestrian import PedestrianDataset
from melbviz.config import MELBVIZ_DATA_PATH, MELBVIZ_COUNTS_CSV_PATH, MELBVIZ_SENSOR_CSV_PATH

data = PedestrianDataset.load(MELBVIZ_COUNTS_CSV_PATH, sensor_csv_path=MELBVIZ_SENSOR_CSV_PATH)
data.to_parquet(MELBVIZ_DATA_PATH / "melbviz.parquet")
