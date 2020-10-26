from melbviz.pedestrian import PedestrianDataset
from melbviz.config import DATA_PATH, COUNTS_CSV_PATH, SENSOR_CSV_PATH

data = PedestrianDataset.load(COUNTS_CSV_PATH, sensor_csv_path=SENSOR_CSV_PATH)
data.to_parquet(DATA_PATH / "melbviz.parquet")
