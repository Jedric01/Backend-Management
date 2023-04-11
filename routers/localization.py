from fastapi import APIRouter, Query
from pydantic import Required
from typing_extensions import Annotated
import json
import numpy as np

from models import gateway_localize_model
from typing import List

from util.localization_engine import Localization_Engine

router = APIRouter(prefix='/localization')
engine = Localization_Engine()

@router.get('/distance')
async def get_radius(rssi: float):
    return engine.rssi_distance(rssi)

@router.post('/localize')
async def localize(gateways: List[gateway_localize_model] = Required):
    # TODO: Try to use fewell's localization algorithm
    return engine.localize(gateways)
    
