from pydantic import BaseModel


class LogInformations(BaseModel):
    username: str
    password: str


class GameInformations(BaseModel):
    name: str
    description: str
    genre: str
    annee: int
    pegi: int
