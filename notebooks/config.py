import os
from pathlib import Path


PEDESTRIAN_DATA_PATH = os.getenv(
    "PEDESTRIAN_DATA_PATH",
    Path.home()
    / "data"
    / "Pedestrian_Counting_System___2009_to_Present__counts_per_hour_.csv",
)
