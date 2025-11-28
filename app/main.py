# backend/app/main.py
from fastapi import FastAPI
from app.database import database, engine, metadata
from app.routers.word import router as word_router
from app.routers.validate import router as validate_router

metadata.create_all(engine)

app = FastAPI(title="Worddee.ai API")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# รวม routers
app.include_router(word_router)
app.include_router(validate_router)

@app.get("/")
def root():
    return {"message": "Worddee backend running!"}
