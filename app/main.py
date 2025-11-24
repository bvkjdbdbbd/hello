from fastapi import FastAPI
from app.db.base import Base 
from app.db.database import engine 
from app.db import models 

from app.api.v1 import tickets
from app import web
from app.db.init_db import seed_data 

from app.admin_panel import setup_admin

def create_tables():
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="Guest Parking QR System", version="1.0.0")

app.include_router(tickets.router) 
app.include_router(web.router)

setup_admin(app, engine)

create_tables()
seed_data() 

@app.get("/")
def read_root():
    return {"message": "Parking QR API is running!"}