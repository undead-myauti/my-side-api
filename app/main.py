import logging
from fastapi import FastAPI
import uvicorn

from app.models.db_tables import Base, engine
from app.routes import user, room

app = FastAPI(debug=True)
app.include_router(user.router)
app.include_router(room.router)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s - %(name)s - %(message)s"
)

logging.getLogger("passlib.handlers.bcrypt").setLevel(logging.WARNING)

logger = logging.getLogger("uvicorn")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")