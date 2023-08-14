from datetime import datetime
from typing import Any

from pydantic import BaseModel


class DurationCounts(BaseModel):
    sec_10: float
    sec_10_30: float
    sec_30: float


class PhoneDataSchema(BaseModel):
    phone: str
    cnt_all_attempts: float
    cnt_att_dur: DurationCounts
    min_price_att: float
    max_price_att: float
    avg_dur_att: float
    sum_price_att_over_15: float


class ResponseSchema(BaseModel):
    correlation_id: int
    status: str = "Complete"
    task_received: str = str(datetime.now())
    _from: str = "report_service"
    _to: str = "client"
    data: list[dict[str, Any]]
    total_duration: str
