from pydantic import BaseModel, Field
from datetime import datetime

# Value Object: ห้ามใช้ str ตรงๆ
class LicensePlate(BaseModel):
    value: str = Field(..., min_length=1, max_length=10)

# Entity: ที่จอดรถ
class ParkingTicket(BaseModel):
    license_plate: LicensePlate
    entry_time: datetime
    version: int = 1 # ป้องกันข้อมูลชนกัน (optimistic Locking)

    