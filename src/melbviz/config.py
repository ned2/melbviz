import os
from pathlib import Path


GOOGLE_GEO_KEY = os.getenv("GOOGLE_GEO_KEY")

MAPBOX_KEY = os.getenv("MAPBOX_KEY")

MELBVIZ_DATA_PATH = Path(os.getenv("MELBVIZ_DATA_PATH", Path.home() / "melbviz_data"))

MELBVIZ_COUNTS_CSV_PATH = ( 
    MELBVIZ_DATA_PATH / "Pedestrian_Counting_System_-_Monthly__counts_per_hour_.csv"
)

MELBVIZ_SENSOR_CSV_PATH = MELBVIZ_DATA_PATH / "Pedestrian_Counting_System_-_Sensor_Locations.csv"

MELBVIZ_CLEANED_DATA_PATH = MELBVIZ_DATA_PATH / "melbviz.parquet"
