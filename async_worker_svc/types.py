from typing import Any, Optional

from pydantic import BaseModel


class IncomingMessage(BaseModel):
    id: str
    command: str
    args: list


class OutgoingMessage(BaseModel):
    id: str
    result: Any
    error: Optional[str] = None
