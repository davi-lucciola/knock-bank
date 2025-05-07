from pydantic import BaseModel, Field


class TokenIn(BaseModel):
    cpf: str = Field(min_length=11, max_length=11)
    password: str


class TokenOut(BaseModel):
    accessToken: str
    type: str = 'bearer'
