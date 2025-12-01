from pydantic import BaseModel
from typing import Optional, List

class WppText(BaseModel):
    body: str

