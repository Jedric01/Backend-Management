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
    # msg: str

@dataclasses.dataclass
class gateway_out_model():
    gateway_eui: str
    elpased_time: float
    exception: Union[str, None] = None
    payload: Union[data_payload, None] = None

class gateway_localize_model(BaseModel):
    lattitude: float
    longitude: float
    rssi: float