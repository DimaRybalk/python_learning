

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas.rules import Rule, RuleCreate, RuleUpdate


router = APIRouter(

    prefix="/rules", 
    tags=["Rules"]
)


@router.get("/", response_model=list[Rule])
def get_rules(db: Session = Depends(get_db)):
    query = select(models.Rule)
    rules = db.execute(query).scalars().all()
    return rules


@router.delete("/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.get(models.Rule, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    db.delete(rule)
    db.commit()

    return rule


@router.patch("/{rule_id}")
def patch_rule(rule_update: RuleUpdate, rule_id: int, db: Session = Depends(get_db)):
    rule = db.get(models.Rule, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    data_update = rule_update.model_dump(exclude_unset=True)
    for key, value in data_update.items():
        setattr(rule, key, value)
    db.commit()
    db.refresh(rule)
    return rule


@router.post("/", response_model=Rule)
def create_rule(rule: RuleCreate, db: Session = Depends(get_db)):
    sensor = db.get(models.Device, rule.sensor_id)
    if not sensor:
        raise HTTPException(
            status_code=404, detail=f"Sensor with id {rule.sensor_id} not found"
        )

    target = db.get(models.Device, rule.action_device_id)
    if not target:
        raise HTTPException(
            status_code=404,
            detail=f"Action device with id {rule.action_device_id} not found",
        )

    db_rule = models.Rule(**rule.model_dump())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule