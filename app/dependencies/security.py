import logging
import datetime

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import ExpiredSignatureError, JWTError, jwt
from app.models.db_tables import User, Session

db = Session()
logger = logging.getLogger(__name__)

SECRET_KEY = "89asd8asd7762d1b12i3i1209501op2n120893081250521389y738"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(email: str):
    """
    Creates a new access token based on user email

    Params: 
        {
            email: str
        }

    Response:
        JWT_TOKEN
    """
    logger.debug("Creating access token")
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
    jwt_data = {"sub": str(email), "exp": expire}
    encoded_jwt = jwt.encode(jwt_data, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_password_hash(password: str) -> str:
    return pswd_context.hash(password)

def verify_password(plain_password:str, hashed_password: str) -> bool:
    return pswd_context.verify(plain_password, hashed_password)

async def get_user(email: str)-> User | None:
    """
    Get user from database based on his email

    Params:
        {
            email: str
        }

    Response:
        user: User
        Failed fetching user from database
    """
    logger.debug("Fetching user from database", extra={"email": email})
    try:
        user = db.query(User).where(User.email == email).first()
        if user:
            logger.debug("User found in database", extra={"user": user})
            return user
    except:
        return "Failed fetching user from database"

async def authenticate_user(email: str, password: str):
    """
    Authenticate user using his email and password

    Params:
        {
            email: xpto@xpto.com
            password: xpto
        }

    Response:
        401 - Could not validate credentials
        200 - user: User
    """
    logger.debug("Authenticating user", extra={"email": email})
    user = await get_user(email)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user

async def get_current_user(token: str):
    """
    Returns current user based on jwt token

    Params:
        {
            token: JWT_TOKEN
        }

    Response:
        401 - Could not validate credentials | Token expired
        200 - user: User
    """
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )

    except ExpiredSignatureError as error:
        raise HTTPException(
            status_code=401,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"}
        ) from error
    except JWTError as error:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        ) from error

    user = await get_user(email=email)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user