import os
from pathlib import Path


MAPBOX_KEY = os.getenv("MELBVIZ_MAPBOX_KEY")

MELBVIZ_DATA_PATH = Path(os.getenv("MELBVIZ_DATA_PATH", Path.home() / "melbviz_data"))

MELBVIZ_COUNTS_CSV_PATH = (
    MELBVIZ_DATA_PATH / "Pedestrian_Counting_System_-_Monthly__counts_per_hour_.csv"
)

MELBVIZ_SENSOR_CSV_PATH = (
    MELBVIZ_DATA_PATH / "Pedestrian_Counting_System_-_Sensor_Locations.csv"
)

MELBVIZ_CLEANED_DATA_PATH = MELBVIZ_DATA_PATH / "melbviz.parquet"
