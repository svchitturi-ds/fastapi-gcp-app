from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn
from uvicorn import lifespan
from  models import item_model as models
from schemas import items_schema as schemas
import crud
from databases.postgres import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# app = FastAPI(title="GCP FastAPI CRUD API")
app = FastAPI(
    title="GCP FastAPI APP",
    description = "GCP API Agent",
    summary= "Service to get a code as per the prompt for quick protoyping usecases",
    docs_url="/gcp/api/v1/docs",
    redoc_url="/gcp/api/v1/redoc",
    openapi_url="/gcp/api/v1/openapi.json",
    openapi_version= "3.1.0",
    version="0.0.1",
    # contact={
    #     "name": "Randomtrees",
    #     "url" : "https://randomtrees.com/"},
    # license_info={"name": "RT-weave-agent - Randomtrees"},
    # lifespan= lifespan
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)

@app.get("/items")
def read_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.delete_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Deleted successfully"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8080)