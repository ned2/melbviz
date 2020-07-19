import os
from pathlib import Path


GOOGLE_GEO_KEY = os.getenv("GOOGLE_GEO_KEY")

MAPBOX_KEY = os.getenv("MAPBOX_KEY")

DATA_PATH = Path("..") / "data"

COUNTS_PATH = (
    DATA_PATH / "Pedestrian_Counting_System___2009_to_Present__counts_per_hour_.csv"
)

SENSOR_PATH = DATA_PATH / "Pedestrian_Counting_System_-_Sensor_Locations.csv"
