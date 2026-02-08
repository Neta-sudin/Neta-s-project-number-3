from fastapi import FastAPI
2from controller.poll_controller import router as poll_router
from repository.database import database

app = FastAPI(
    title="Poll Service API",
    description="Microservice for managing poll questions, answers, and statistics",
    version="1.0.0"
)

app.include_router(poll_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {
        "service": "Poll Service",
        "status": "running",
        "version": "1.0.0"
    }

