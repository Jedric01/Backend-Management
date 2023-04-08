from pydantic import BaseModel

class gateway_commands: 
    PREFIX = '/gateway/control'
    PING = 'PING'
    REBOOT = 'REBOOT'
    START = 'START'
    STOP = 'STOP'

# define models here