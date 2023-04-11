from fastapi import APIRouter, Query
from pydantic import Required
from typing_extensions import Annotated
import json
import numpy as np

router = APIRouter(prefix='/localization')
PREFIX_TRAIN_DATA = 'train_data/processed'
train_data = {}

# convert rssi to distance/radius, by linear interpolating training data
def rssi_distance(rssi: float, tx_power: int = 10):
    # get first index, at which rssi from training data is lower than the given rssi value
    rssi_data = np.array(train_data['rssi'])
    distance = np.array(train_data['distance'])
    idx = np.argmax(rssi_data < rssi)
    # Generalized De-Moive's linear interpolation 
    # m = (y_1-y_0)/(x_1 - x_0)
    slope = (rssi_data[idx] - rssi_data[idx - 1])/(distance[idx] - distance[idx - 1])
    # (y - y_0) = m * (x - x_0) => x = (y - y_0)/m + x_0, where x is radius
    radius = (rssi - rssi_data[idx - 1])/slope + distance[idx - 1]
    print(f'interpolating between {distance[idx - 1]} and {distance[idx]}')
    print('radius:', radius)
    return radius

@router.on_event('startup')
async def read_train_data():
    with open(f'{PREFIX_TRAIN_DATA}/t8_tx10.json', 'r') as f1, open(f'{PREFIX_TRAIN_DATA}/t20_tx10.json') as f2, open(f'{PREFIX_TRAIN_DATA}/t8_tx15.json', 'r') as f3:
        data_str = json.load(f1)
        data = json.loads(data_str)
        train_data['rssi'] = data['rssi']
        train_data['distance'] = data['distance']

@router.get('/distance')
async def localize(rssi: float):
    return rssi_distance(rssi)