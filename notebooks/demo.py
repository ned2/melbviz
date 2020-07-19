from config import COUNTS_PATH, SENSOR_PATH
from pedestrian import PedestrianDataset
from prototype import PedestrianDemo



class Demo(PedestrianDataset, PedestrianDemo):
    pass


demo = Demo.load(COUNTS_PATH, sensor_csv_path=SENSOR_PATH, debug=True)
demo.prototype()
