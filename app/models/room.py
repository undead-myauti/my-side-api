from pydantic import BaseModel

class Room(BaseModel):
    id: int | None = None
    name: str
    capacity: int
    location: str