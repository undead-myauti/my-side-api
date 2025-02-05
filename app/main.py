from fastapi import FastAPI
import uvicorn

from app.models.db_tables import Base, engine
from app.routes import user

app = FastAPI()
app.include_router(user.router)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)