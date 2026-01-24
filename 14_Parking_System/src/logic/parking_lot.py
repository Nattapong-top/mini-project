import math
from datetime import datetime

class ParkingLot:
    def __init__(self):
        self.hourly_rate = 20
        self.max_daily_fee = 200
        self.lost_ticket_penalty = 100

    def calculate_fee(self, entry_time_str, is_lost=False):
        # แปลงข้อความเวลาเป็น Object ของ Python
        entry_time = datetime.strptime(entry_time_str, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        duration = now - entry_time
        
        # ปัดเศษชั่วโมงขึ้น
        total_seconds = duration.total_seconds()
        hours = math.ceil(total_seconds / 3600)

        # 1. ลอจิกปกติ: 2 ชม. แรกฟรี
        actual_fee = 0
        if hours > 2:
            actual_fee = (hours - 2) * self.hourly_rate
            
        # 2. ลอจิกเพดานราคา: ไม่เกิน 200
        if actual_fee > self.max_daily_fee:
            actual_fee = self.max_daily_fee

        # 3. ลอจิกระดับเซียนของป๋า: ถ้าบัตรหาย ถ้าน้อยกว่า 100 คิด 100
        if is_lost:
            return max(self.lost_ticket_penalty, actual_fee)
        
        return actual_fee