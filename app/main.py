from fastapi import FastAPI

from app.api.routes import theater

app = FastAPI(title="Movie Booking System")

app.include_router(theater.router)