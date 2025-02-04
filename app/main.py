from fastapi import FastAPI
import uvicorn
from app.models.models import Base, engine

app = FastAPI()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)