import math
from pydantic import BaseModel, Field
from datetime import datetime

class PricingPolicy(BaseModel):
    hourly_rate: int = 20
    free_hour: int = 2
    hour_limit: int = 24
    max_daily: int = 200
    lost_ticket_penalty: int = 100

class OverLimitError(Exception):
    '''Exception สำหรับกรณีจอดรถเกินเวลาที่กำหนด'''
    pass

class LicensePlate(BaseModel):
    value: str = Field(..., min_length=1, max_length=10)

class ParkingTicket(BaseModel):
    license_plate: LicensePlate
    entry_time: datetime
    version: int = 1

    def calculate_fee(self, current_time: datetime, Policy: PricingPolicy, is_lost: bool = False) -> int:
        # 1. คำนวณชั่วโมง
        duration = current_time - self.entry_time
        hours = math.ceil(duration.total_seconds() / 3600)

        # 2. Guard Clause: เช็กขีดจำกัดเวลาก่อน
        if hours > Policy.hour_limit:
            raise OverLimitError('จอดเกินเวลา กรุณาติดต่อพนักงาน')

        # 3. คำนวณเงินพื้นฐาน (ใช้ max(0, ...) เพื่อไม่ให้เงินติดลบ)
        billable_hours = max(0, hours - Policy.free_hour)
        base_fee = billable_hours * Policy.hourly_rate

        # 4. คุมเพดานราคา (ไม่เกิน 200)
        final_fee = min(base_fee, Policy.max_daily)

        # 5. กรณีบัตรหาย: เลือกค่าที่แพงกว่าระหว่าง ค่าปรับ กับ ค่าจอดจริง
        if is_lost:
            return max(Policy.lost_ticket_penalty, final_fee)
            
        return final_fee