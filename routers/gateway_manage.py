from fastapi import APIRouter, Query, Depends, Request, status
from typing_extensions import Annotated

from util.mqtt import MQTTClient
from util import parser
from dependencies import gateway_query_params

import asyncio
from concurrent.futures import ThreadPoolExecutor
from models import *

# initialize required objects
MAX_TIMEOUT = 10
mqtt = MQTTClient('broker.emqx.io',1883)
executor = ThreadPoolExecutor(5)
router = APIRouter(prefix=gateway_commands.PREFIX, dependencies=[Depends(gateway_query_params)])
    
@router.get("/ping", status_code=status.HTTP_200_OK)
async def ping(request: Request):
    # publish to mqtt  topic
    mqtt.publish(f'{gateway_commands.PREFIX}/{request.state.eui}', gateway_commands.PING)

    #await response from gateway
    try:
        event_loop = asyncio.get_event_loop()
        # run in new thread
        future = event_loop.run_in_executor(executor, lambda: mqtt.sub_and_wait(f'{gateway_commands.PREFIX}/{request.state.eui}', MAX_TIMEOUT))
        response, elapsed_time = await future
        if response is None:
            raise TimeoutError('Response took too long!')
    except Exception as e:
        return gateway_out_model(request.state.eui, elapsed_time, exception=str(e))
    
    return gateway_out_model(request.state.eui, elapsed_time)

@router.get('/reboot')
async def reboot(request: Request, config_file: str, server_address: str):
    # publish to mqtt topic 
    mqtt.publish(f'{gateway_commands.PREFIX}/{request.state.eui}', gateway_commands.REBOOT)



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

@router.get('/temp')
async def get_temp(request: Request):
    # publish to mqtt  topic
    mqtt.publish(f'{gateway_commands.PREFIX}/{request.state.eui}', gateway_commands.TEMP)

    # await response from gateway
    try:
        event_loop = asyncio.get_event_loop()
        # run in new thread
        future = event_loop.run_in_executor(executor, lambda: mqtt.sub_and_wait(f'{gateway_commands.PREFIX}/{request.state.eui}', MAX_TIMEOUT))
        response, elapsed_time = await future
        if response is None:
            raise TimeoutError('Response took too long!')
    except Exception as e:
        return gateway_out_model(request.state.eui, elapsed_time, exception=str(e))
    
    temp = parser.parse_temp(response.payload)
    return gateway_out_model(request.state.eui, elapsed_time, payload = data_payload(temp=temp))

@router.get('/uptime')
async def get_uptime(request: Request):
     # publish to mqtt  topic
    mqtt.publish(f'{gateway_commands.PREFIX}/{request.state.eui}', gateway_commands.UPTIME)

    # await response from gateway
    try:
        event_loop = asyncio.get_event_loop()
        # run in new thread
        future = event_loop.run_in_executor(executor, lambda: mqtt.sub_and_wait(f'{gateway_commands.PREFIX}/{request.state.eui}', MAX_TIMEOUT))
        response, elapsed_time = await future
        if response is None:
            raise TimeoutError('Response took too long!')
    except Exception as e:
        return gateway_out_model(request.state.eui, elapsed_time, exception=str(e))
    
    uptime = parser.parse_uptime(response.payload)
    return gateway_out_model(request.state.eui, elapsed_time, payload = data_payload(uptime=uptime))
