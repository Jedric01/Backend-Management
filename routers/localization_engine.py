from fastapi import APIRouter, Query
from pydantic import Required
from typing_extensions import Annotated

router = APIRouter(prefix='/localization')