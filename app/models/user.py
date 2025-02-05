from pydantic import BaseModel

class User(BaseModel):
    id: int | None = None
    email: str
    name: str

class UserIn(User):
    password: str