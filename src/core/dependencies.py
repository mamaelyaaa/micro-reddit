from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from .database import db_helper

SessionDep = Annotated[AsyncSession, Depends(db_helper.session_getter)]
