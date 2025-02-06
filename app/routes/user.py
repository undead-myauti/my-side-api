from fastapi import APIRouter, HTTPException
import logging

from fastapi.responses import JSONResponse
from app.models.user import UserIn
from app.dependencies.security import authenticate_user, create_access_token, get_user, get_password_hash
from app.models.db_tables import User, Session

logger = logging.getLogger(__name__)

router = APIRouter()
db = Session()

@router.post("/register", status_code=201)
async def register(user: UserIn):
    """
    Register a new user in database

    Params:
        {
            email: "xpto@xpto.com",
            password: xpto,
            name: xpto
        }

    Response:
        200 - User registered
        400 - Error registering user
    """
    if await get_user(user.email):
        raise HTTPException(
            status_code = 400, 
            detail = "User already exists"
        )

    try:
        hashed_pswd = get_password_hash(user.password)

        db.add(User(name=user.name, password=hashed_pswd, email=user.email))
        db.commit()
        logger.debug(f"User registered: {user}")

        return JSONResponse(status_code=200, content="User registered")
    except:
        db.rollback()
        logger.debug(msg="Error registering user")
        raise HTTPException(status_code=400, detail="Error registering user")
    finally:
        db.close()

@router.post("/token")
async def login(user: UserIn):
    """
    This route authenticate an user with his email and password and generates a new JWT token

    Params:
        {
            email: "xpto@xpto.com",
            password: xpto,
            name: xpto
        }

    Response:
        {
            access_token: JWT_TOKEN,
            token_type: bearer
        }
    """
    user = await authenticate_user(user.email, user.password)

    access_token = create_access_token(user.email)
    logger.debug(f"User token created")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/user/{email}")
async def get_user(email: str):
    """
    This route returns an user based on his email

    Params:
        {
            email: xpto@xpto.com
        }
    
    Response:
        200 - user: User
        404 - User not found
        400 - Error getting user
    """
    try:
        user = db.query(User).where(User.email == email).first()
        if user:
            return {
                "id": user.id,
                "email": user.email,
                "name": user.name
            } 
    except:
        logging.exception("Error getting user")
        raise HTTPException(status_code=400, detail="Error getting user")