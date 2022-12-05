from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models,crud,schemas
from test_database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/")
def create_user(db: Session = Depends(get_db)):
    return {"TEMP":"TEMP"}
