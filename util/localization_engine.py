import numpy as np
import json


class Localization_Engine():
    PREFIX_TRAIN_DATA = 'train_data/processed'
    train_data = {}

    def __init__(self) -> None:
        with open(f'{self.PREFIX_TRAIN_DATA}/t8_tx10.json', 'r') as f1, open(f'{self.PREFIX_TRAIN_DATA}/t20_tx10.json') as f2, open(f'{self.PREFIX_TRAIN_DATA}/t8_tx15.json', 'r') as f3:
            data_str = json.load(f1)
            data = json.loads(data_str)
            self.train_data['rssi'] = data['rssi']
            self.train_data['distance'] = data['distance']

    # convert rssi to distance/radius, by linear interpolating training data
    def rssi_distance(self, rssi: float, tx_power: int = 10):
        # get first index, at which rssi from training data is lower than the given rssi value
        rssi_data = np.array(self.train_data['rssi'])
        distance = np.array(self.train_data['distance'])
        idx = np.argmax(rssi_data < rssi)
        # Generalized De-Moive's linear interpolation 
        # m = (y_1-y_0)/(x_1 - x_0)
        slope = (rssi_data[idx] - rssi_data[idx - 1])/(distance[idx] - distance[idx - 1])
        # (y - y_0) = m * (x - x_0) => x = (y - y_0)/m + x_0, where x is radius
        radius = (rssi - rssi_data[idx - 1])/slope + distance[idx - 1]
        print(f'interpolating between {distance[idx - 1]} and {distance[idx]}')
        print('radius:', radius)
        return radius