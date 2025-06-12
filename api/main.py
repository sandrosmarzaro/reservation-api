from fastapi import FastAPI

from api.routers import property, reservation

from .db.base import Base
from .db.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Properties Reservation API of Seazone',
    description='API to for short or medium-term stays.',
    version='0.1.0',
)

app.include_router(property.router)
app.include_router(reservation.router)
