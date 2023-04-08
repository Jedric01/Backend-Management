from enum import Enum 
from fastapi import FastAPI, Path, Query

# from services.gateway_manage import gateway_manage, localization_engine

from contextlib import asynccontextmanager
from routers import gateway_manage, localization_engine

app = FastAPI()
app.include_router(gateway_manage.router)
app.include_router(localization_engine.router)



