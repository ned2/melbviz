import os
from pathlib import Path


MAPBOX_KEY = os.getenv("MELBVIZ_MAPBOX_KEY")

MELBVIZ_DATA_PATH = Path(os.getenv("MELBVIZ_DATA_PATH", Path.home() / "melbviz_data"))

MELBVIZ_COUNTS_CSV_PATH = (
    MELBVIZ_DATA_PATH
    / "Pedestrian_Counting_System_Monthly_counts_per_hour_may_2009_to_14_dec_2022.csv"
)

MELBVIZ_SENSOR_CSV_PATH = (
    MELBVIZ_DATA_PATH / "pedestrian-counting-system-sensor-locations.csv"
)

MELBVIZ_CLEANED_DATA_PATH = MELBVIZ_DATA_PATH / "melbviz.parquet"
