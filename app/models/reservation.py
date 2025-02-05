from pydantic import BaseModel

class Reservation(BaseModel):
    id: int | None = None
    owner_email: str
    room_id: int
    start_time: str
    end_time: str