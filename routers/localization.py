from fastapi import APIRouter, Query
from pydantic import Required
from typing_extensions import Annotated
import json
import numpy as np

from models import gateway_localize_model, gateway_rssi_in, gateway_rssi_out
from typing import List

from util.localization_engine import Localization_Engine

router = APIRouter(prefix='/localization')
engine = Localization_Engine()

@router.post('/distance')
async def get_radius(gateways: List[gateway_rssi_in]) -> List[gateway_rssi_out]:
    out = []
    for g in gateways:
        est_distance = engine.rssi_to_distance(g.rssi)
        out.append(gateway_rssi_out(gateway_eui=g.gateway_eui, device_eui = g.device_eui, distance=est_distance))
    return out

@router.post('/trilaterate')
async def localize(gateways: List[gateway_localize_model] = Required):
    # TODO: Try to use fewell's localization algorithm
    return engine.localize(gateways)
    
