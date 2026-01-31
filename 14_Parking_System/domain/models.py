import math
from pydantic import BaseModel, Field
from datetime import datetime


# ขอกำหนดต่างๆ bissiness
class PricingPolicy(BaseModel):
    hourly_rate: int = 40
    free_hour: int = 2

# Value Object: ห้ามใช้ str ตรงๆ
class LicensePlate(BaseModel):
    value: str = Field(..., min_length=1, max_length=10)

# Entity: ที่จอดรถ
class ParkingTicket(BaseModel):
    license_plate: LicensePlate
    entry_time: datetime
    version: int = 1 # ป้องกันข้อมูลชนกัน (optimistic Locking)

    def calculate_fee(self, current_time: datetime, Policy: PricingPolicy) -> int:
        duration = current_time - self.entry_time
        total_seconds = duration.total_seconds()
        
        hours = math.ceil(total_seconds / 3600)
        
        # ฟรี 2 ชั่งโมงแรก ชั่วโมงต่อไป 40 บาท
        if hours <= Policy.free_hour:
            return 0
        else:
            fee = (hours - 2) * Policy.hourly_rate
            return fee
