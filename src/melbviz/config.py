import os
from pathlib import Path


GOOGLE_GEO_KEY = os.getenv("GOOGLE_GEO_KEY")

MAPBOX_KEY = os.getenv("MAPBOX_KEY")

ROOT_PATH = Path(os.path.abspath(os.path.dirname(__file__)))

DATA_PATH = Path(os.getenv("DATA_PATH", ROOT_PATH / ".." / "data"))

COUNTS_CSV_PATH = ( 
    DATA_PATH / "Pedestrian_Counting_System_-_Monthly__counts_per_hour_.csv"
)

SENSOR_CSV_PATH = DATA_PATH / "Pedestrian_Counting_System_-_Sensor_Locations.csv"

CLEANED_DATA_PATH = DATA_PATH / "melbviz.parquet"
