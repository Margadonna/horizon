from Data_model import *
from Modeling import *
from recomendation import *


def main ():
    config = Config()
    conf = config.read_config('config.ini')
    dataset = DataSeriesDataset(conf, 'Horizon-data')