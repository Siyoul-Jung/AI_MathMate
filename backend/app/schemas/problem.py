from pydantic import BaseModel
from typing import List, Optional

class LogItem(BaseModel):
    student_id: str
    standard_id: str
    step_type: str
    success_status: str

class ProblemResponse(BaseModel):
    p_id: str
    mode: str
    level: int
    content: dict # This can be further refined if the engine output structure is fixed
