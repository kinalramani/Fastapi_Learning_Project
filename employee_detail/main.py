from fastapi import FastAPI
from src.routers.employee import employee


app=FastAPI()

app.include_router(employee)