
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, select
import models
from database import get_db
from schemas.device import Device, DeviceCreate, DeviceStats, DeviceUpdate, DeviceStatus
from schemas.measurments import Measurement

router = APIRouter(

    prefix="/devices", 
    tags=["Devices"]
)

@router.get("/", response_model=list[Device])
def get_devices(db: Session = Depends(get_db)):
    query = select(models.Device)
    devices = db.execute(query).scalars().all()

    return devices

@router.get("/{device_id}/stats",response_model=DeviceStats)
def get_device_stats(device_id:int,db: Session = Depends(get_db)):
    device = db.get(models.Device, device_id)
    if not device:
        raise HTTPException(status_code=404,detail="No devices found")
    query = select(func.avg(models.Measurement.value).label("average"),
        func.max(models.Measurement.value).label("maximum"),
        func.min(models.Measurement.value).label("minimum"),
        func.count(models.Measurement.id).label("count")).where(models.Measurement.device_id == device_id)
    stats = db.execute(query).mappings().first()
    return stats

@router.get("/{device_id}/measurements",response_model=list[Measurement])
def get_device_measurements(device_id:int,db: Session = Depends(get_db)):
    device = db.get(models.Device, device_id)
    if not device:
        raise HTTPException(status_code=404,detail="No devices found")
    query = select(models.Measurement).where(models.Measurement.device_id == device_id)
    measurements = db.execute(query).scalars().all()
    return measurements


@router.post("/", response_model=Device)
def create_device(
    device: DeviceCreate,
    db: Session = Depends(get_db),
):
    db_device = models.Device(
        name=device.name,
        type=device.type,
    )

    db.add(db_device)
    db.commit()
    db.refresh(db_device)

    return db_device


@router.get("/{id}", response_model=Device)
def get_device_by_id(device_id: int, db: Session = Depends(get_db)):
    device = db.get(models.Device, device_id)

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return device


@router.delete("/{id}", response_model=Device)
def delete_device_by_id(device_id: int, db: Session = Depends(get_db)):
    device = db.get(models.Device, device_id)

    if not device:
        raise HTTPException(status_code=404, detail="No device to delete")

    db.delete(device)
    db.commit()

    return device


@router.patch("/{device_id}/status", response_model=Device)
def patch_device(device_id: int, status: DeviceStatus, db: Session = Depends(get_db)):
    device = db.get(models.Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="No device to patch")
    device.status = status
    db.commit()
    db.refresh(device)
    return device


@router.patch("/{device_id}", response_model=Device)
def update_device(
    device_update: DeviceUpdate, device_id: int, db: Session = Depends(get_db)
):
    device = db.get(models.Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="No device to patch")
    update_data = device_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(device, key, value)
    db.commit()
    db.refresh(device)
    return device