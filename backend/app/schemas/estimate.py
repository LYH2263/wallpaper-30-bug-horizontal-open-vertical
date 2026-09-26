from typing import Literal, Optional

from pydantic import BaseModel


class EstimateRequest(BaseModel):
    wall_id: int
    roll_id: int
    save: bool = False
    note: str = ""
    # None → fall back to the system default orientation from settings.
    orientation: Optional[Literal["vertical", "horizontal"]] = None
