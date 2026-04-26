from typing import Any, Optional
from app.Schemas.underwriter_request import UnderWriterRequest
from app.models.MatchResult import MatchStatus


class UnderwriterResponse(UnderWriterRequest):
    match_id: int
    lender_name: str
    program_name: Optional[str]
    is_eligible: bool
    match_score: float
    status: MatchStatus
    criteria_results: Any

    class Config:
        from_attributes = True
