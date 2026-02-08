from fastapi import FastAPI
from controller.user_controller import router as user_router
from repository.database import database

app = FastAPI(
    title="User Service API",
    description="Microservice for managing users in the poll system",
    version="1.0.0"
)

app.include_router(user_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {
        "service": "User Service",
        "status": "running",
        "version": "1.0.0"
    }

