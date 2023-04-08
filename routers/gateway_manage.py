from fastapi import APIRouter, Query, Depends, Request, status
from typing_extensions import Annotated

from mqtt import MQTTClient
from paho.mqtt import subscribe
from dependencies import gateway_query_params

import json
import asyncio

from concurrent.futures import ThreadPoolExecutor
from models import gateway_commands

# tp = ThreadPoolExecutor(5)
mqtt = MQTTClient('broker.emqx.io', 1883)
router = APIRouter(prefix=gateway_commands.PREFIX, dependencies=[Depends(gateway_query_params)])

@router.on_event('startup')
async def init_mqtt_client():
    mqtt.connect_mqtt()

@router.get("/ping", status_code=status.HTTP_200_OK)
async def ping(request: Request):
    # publish to mqtt  topic
    mqtt.publish(f'{gateway_commands.PREFIX}/{request.state.eui}', gateway_commands.PING)

    # await response from gateway
    try:
        event_loop = asyncio.get_event_loop()
        # run in new thread
        future = event_loop.run_in_executor(tp, lambda: subscribe.simple(f'{gateway_commands.PREFIX}/{request.state.eui}', hostname='broker.emqx.io', port=1883))
        response = await asyncio.wait_for(future, timeout=5, loop=event_loop)
    except Exception as e:
        return e

    return response.payload

# @router.get('/reboot')
# async def reboot(request: Request, config_file: str, server_address: str):
#     # publish to mqtt topic
#     mqtt.publish(f'{gateway_commands.PREFIX}/{request.state.eui}', )

@router.get('/start', status_code=status.HTTP_200_OK)
async def start(request: Request, config_file: str, server_address: str):
    mqtt.publish(f'{gateway_commands.PREFIX}/{request.state.eui}', f'{gateway_commands.START};{config_file};{server_address}')
    return 

@router.get('/stop', status_code=status.HTTP_200_OK)
async def stop(request: Request, config_file: str, server_addres: str):
    mqtt.publish(f'{gateway_commands.PREFIX}/{request.state.eui}', f'{gateway_commands.STOP};{config_file};{server_addres}')
    return



# @router.get('/config')
# async def config(request: Request, config: str):

# @router.get('temp')

# @router.get('uptime')