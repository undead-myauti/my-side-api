import logging
import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from jose import jwt, JWTError

from app.models.db_tables import Reservation, Session
from app.models.reservation import Reservation as Reservation_model
from app.dependencies.security import get_current_user, oauth2_scheme, SECRET_KEY, ALGORITHM
from app.routes.room import check_room_availability
from app.routes.user import get_user

logger = logging.getLogger(__name__)

router = APIRouter()
db = Session()

@router.post("/reservations")
async def create_reservation(reservation: Reservation_model):
    """
    Creates a reservation, which contains informations about its owner, the room itself and the hours that the room will be occupied.
    Also verifies if the room is available and if the start time is greater than end time
    
    Params:
         {
            "room_id": 1,
            "user_name": "João Silva",
            "start_time": "2025-01-22T14:00:00",
            "end_time": "2025-01-22T16:00:00",
            "owner": "xpto@xpto.com"
        }
    
    Response:
        400 - Start time should be greater than end time
        400 - Failed registering room {room_id}
        201 - Room {room_id} reserved successfully
    """
    room_availability = await check_room_availability(reservation.room_id, reservation.start_time, reservation.end_time)

    if room_availability.status_code == 404 or room_availability.status_code == 400:
        return JSONResponse(status_code=400, content=json.loads(room_availability.body))

    owner = await get_user(reservation.owner_email)

    try:
        db.add(Reservation(owner=owner.get("id"), room=reservation.room_id, start_time=reservation.start_time, end_time=reservation.end_time))
        db.commit()
        return JSONResponse(status_code=201, content=f"Room {reservation.room_id} reserved successfully")
    except:
        db.rollback()
        logging.exception(f"Failed registering room {reservation.room_id}")
        return JSONResponse(status_code=400, content=f"Failed registering room {reservation.room_id}")
    
@router.delete("/reservations/{id}")
async def delete_reservation(id: int, token: str):
    """
    This route needs a token and an id to delete a reservation from database.
    Only allows the owner of the reservation to delete it.

    Params:
        {
            id: int
            token: str
        }

    Response:
        403 - Permission denied
        400 - Error deleting reservation
        200 - Reservation deleted successfully
    """
    if not token:
        return JSONResponse(status_code=403, content="Permission denied")
    
    reservation = await get_reservation(id)
    current_user = await get_current_user(token)

    try:
        if reservation.owner == current_user.id:
            db.delete(reservation)
            db.commit()
            logging.debug("Reservation deleted successfully")
            return JSONResponse(status_code=200, content="Reservation deleted successfully")
        return JSONResponse(status_code=403, content="Permission denied")
    except:
        logging.debug("Error deleting reservation")
        db.rollback()
        logging.exception(f"Error deleting reservation {reservation.room_id}")
        return JSONResponse(status_code=400, content="Error deleting reservation")

@router.get("/reservation/{id}")
async def get_reservation(id: int):
    """
    Returns a reservation object when an id is given

    Params:
        {
            id: int
        }

    Response:
        404 - Reservation not found
        400 - Error getting reservation
        200 - reservation: Reservation
    """
    try:
        reservation = db.query(Reservation).where(Reservation.id == id).first()
        if reservation:
            return reservation
        return JSONResponse(status_code=404, content="Reservation not found")
    except:
        logging.exception("Error getting reservation")
        return JSONResponse(status_code=400, content="Error getting reservation")