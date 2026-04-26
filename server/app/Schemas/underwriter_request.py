from pydantic import BaseModel


class UnderWriterRequest(BaseModel):
    loan_request_id: int
