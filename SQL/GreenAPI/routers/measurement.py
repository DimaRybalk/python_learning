import operator
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
import models
from schemas.measurments import Measurement, MeasurementCreate


OPS = {">": operator.gt, "<": operator.lt, "==": operator.eq}

router = APIRouter(

    prefix="/measurements", 
    tags=["Measurements"]
)


@router.post("/", response_model=Measurement)
def create_measurment_value(
    measurment: MeasurementCreate, db: Session = Depends(get_db)
):
    device = db.get(models.Device, measurment.device_id)
    if not device:
        raise HTTPException(status_code=404, detail="No device to write in")

    db_measurment = models.Measurement(**measurment.model_dump())

    if db_measurment.value > 100:
        device.status = "error"

    rules = (
        db.execute(
            select(models.Rule).where(models.Rule.sensor_id == measurment.device_id)
        ).scalars().all()
    )

    for rule in rules:

        op_func = OPS.get(rule.operator)

        if op_func and op_func(db_measurment.value, rule.treshold):

            target_device = db.get(models.Device, rule.action_device_id)
            if target_device:

                target_device.status = "active"

    db.add(db_measurment)
    db.commit()
    db.refresh(db_measurment)
    return db_measurment


@router.get("/latest", response_model=list[Measurement])
def get_latest_measurements(db: Session = Depends(get_db)):
    query = select(models.Measurement).order_by(models.Measurement.id.desc()).limit(10)
    measurements = db.execute(query).scalars().all()
    if not measurements:
        raise HTTPException(status_code=404, detail="There are no measurements")
    return measurements


@router.delete("/{measurements_id}",response_model=Measurement)
def delete_measurement(measurements_id:int,db: Session = Depends(get_db)):
    measurement = db.get(models.Measurement, measurements_id)
    if not measurement:
        raise HTTPException(status_code=404,detail="No measurements found")
    db.delete(measurement)
    db.commit()
    
    return measurement