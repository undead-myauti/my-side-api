import datetime
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.models.db_tables import Room, Session
from app.models.room import Room as room_model
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()
db = Session()

@router.post("/rooms")
async def create_room(room: room_model):
    """
    This route creates a new room and returns its information

    Params:
        room: Room

    Return:
        200 - Room Created || 400 - Error creating room
    """

    try:
        db.add(Room(name=room.name, capacity=room.capacity, location=room.location))
        db.commit()

        return JSONResponse(
            status_code=201, 
            content={
                "msg": "Room Created",
                "room_info": {
                    "name": room.name,
                    "capacity": room.capacity,
                    "location": room.location
                }  
            }
        )
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating room! Detail: {error}")
    finally:
        db.close()

@router.get("/rooms")
async def get_rooms():
    """
        This route lists all rooms created

        Return:
            When there's no room created yet: 200 - There's no room created
            When there's at least one room created: List[Room]
            Error: 404 - Error looking for rooms
    """
    try:
        rooms_list = db.query(Room).all()
        if not rooms_list:
            return JSONResponse(status_code=200, content="There's no room created")
        return rooms_list
    except:
        return JSONResponse(status_code=404, content="Error looking for rooms")
    
@router.post("/rooms/{id}/availability")
async def check_room_availability(id: int, start_time: str, end_time: str):
    try:
        room = db.query(Room).where(Room.id == id)
        if not room:
            return JSONResponse(status_code=404, content="Room not found")
    except:
        pass
    pass