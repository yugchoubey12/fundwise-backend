from pydantic import BaseModel

class UserInput(BaseModel):
    sip: int
    years: int
    goal: str
