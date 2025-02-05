from fastapi import APIRouter, HTTPException, status
import logging
from app.models.user import UserIn
from app.dependencies.security import authenticate_user, create_access_token, get_user, get_password_hash
from app.models.db_tables import User, Session
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

router = APIRouter()
db = Session()

@router.post("/register", status_code=201)
async def register(user: UserIn):
    logger.debug(f"Registering user: {user}")

    if await get_user(user.email):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = "User already exists"
        )

    try:
        hashed_pswd = get_password_hash(user.password)

        db.add(User(name=user.name, password=hashed_pswd, email=user.email))
        db.commit()

        raise HTTPException(status_code=status.HTTP_200_OK, detail="User registered")
    except SQLAlchemyError as error:
        db.rollback()
        logger.log(msg="Error registering user")
    finally:
        db.close()

@router.post("/token")
async def login(user: UserIn):
    user = await authenticate_user(user.email, user.password)

    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}