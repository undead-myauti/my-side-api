from datetime import datetime
import json
import logging
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import Date
from app.models.db_tables import Room, Reservation, Session
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
        200 - Room Created
        400 - Error creating room
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
    
@router.get("/rooms/{id}/availability")
async def check_room_availability(id: int, start_time: str, end_time: str):
    """
    Check a room availability looking for a start time and an end time

    Params:
        {
            id: 1,
            start_time: 2025-01-22T14:00:00
            end_time: 2025-01-22T16:00:00
        }

    Response:
        400 - Start time should be greater than end time | Hour conflict reserving room
        404 - Room not found
        200 - Room available
    """
    try:
        room = db.query(Room).where(Room.id == id).first()
        formated_start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
        formated_end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")

        if formated_start_time > formated_end_time:
            return JSONResponse(status_code=400, content="Start time should be greater than end time")
    
        reservations = await get_room_reservations(id)
        reservation_list = json.loads(reservations.body.decode("utf-8"))

        for res in reservation_list:
            if reservations.status_code == 202:
                continue
            formated_res_end_time = datetime.strptime(res["end_time"], "%Y-%m-%dT%H:%M:%S")
            formated_res_start_time = datetime.strptime(res["start_time"], "%Y-%m-%dT%H:%M:%S")
            if formated_start_time < formated_res_end_time and formated_end_time > formated_res_start_time:
                logging.debug(f"Hour conflict reserving room {id}")
                return JSONResponse(status_code=400, content=f"Hour conflict reserving room {id}")
            if not room:
                return JSONResponse(status_code=404, content="Room not found")
        return JSONResponse(status_code=200, content=f"Room {id} available")
    except:
        return JSONResponse(status_code=400, content="Error checking room availability")

@router.get("/rooms/{id}/reservations")
async def get_room_reservations(id: int, date: str | None = None):
    """
    Returns all reservations from a room in a specific date or all the reservations for the room.

    Params:
        {
            "date": "date=2025-01-22" | None
        }

    Response:
        200 - List[Reservations]
        202 - No reservations for this room
        400 - Error looking for reservations
    """
    if date is not None:
        date_formatted = datetime.strptime(date, "%Y-%m-%d").date()

    try:
        if date is not None:
            reservations = db.query(Reservation).filter(Reservation.room == id).filter(Reservation.start_time.cast(Date) == date_formatted).all()
        else:
            reservations = db.query(Reservation).where(Reservation.room == id).all()

        reservations_to_dict = [
            {
                "id": res.id,
                "room_id": res.room,
                "owner": res.owner,
                "start_time": res.start_time.isoformat(),
                "end_time": res.end_time.isoformat(),
            } for res in reservations
        ]
        
        if reservations:
            return JSONResponse(status_code=200, content=reservations_to_dict)
        
        return JSONResponse(status_code=202, content="No reservations for this room")
    except:
        return JSONResponse(status_code=400, content="Error looking for reservations")