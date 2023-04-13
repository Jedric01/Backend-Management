from pydantic import BaseModel, dataclasses, Field
from dataclasses import field
from typing import Union

class gateway_commands: 
    PREFIX = '/gateway/control'
    PING = 'PING'
    REBOOT = 'REBOOT'
    START = 'START'
    STOP = 'STOP'
    TEMP = 'TEMP'
    UPTIME = 'UPTIME'

# define models here
@dataclasses.dataclass
class data_payload():
    temp: Union[float, None] = None
    uptime: Union[float, None] = None
    feedback: Union[str, None] = None
    # msg: str

@dataclasses.dataclass
class gateway_out_model():
    gateway_eui: str
    elpased_time: float
    exception: Union[str, None] = None
    payload: Union[data_payload, None] = None

class base_gateway_model(BaseModel):
    gateway_eui: str
    device_eui: str

class gateway_localize_model(base_gateway_model):
    lattitude: float
    longitude: float
    rssi: float

class gateway_rssi_in(base_gateway_model):
    rssi: int

class gateway_rssi_out(base_gateway_model):
    distance: float