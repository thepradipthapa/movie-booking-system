from fastapi import FastAPI

from app.api.routes import auth, movie, screen, seat, show, theater

app = FastAPI(title="Movie Booking System")

app.include_router(auth.router)
app.include_router(theater.router)
app.include_router(screen.router)
app.include_router(movie.router)
app.include_router(seat.router)
app.include_router(show.router)