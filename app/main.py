from fastapi import FastAPI

from app.api.routes import movie, screen, theater

app = FastAPI(title="Movie Booking System")

app.include_router(theater.router)
app.include_router(screen.router)
app.include_router(movie.router)