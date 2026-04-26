from typing import Any
from app.models.MatchResult import MatchStatus
from underwriter_request import UnderWriterRequest

class UnderwriterResponse(UnderWriterRequest):
    match_id: int
    class Config:
        from_attributes = True
