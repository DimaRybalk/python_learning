from fastapi import FastAPI
import models
from database import engine
from routers import device, measurement, rules


models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="GreenApi")

app.include_router(device.router)
app.include_router(measurement.router)
app.include_router(rules.router)




