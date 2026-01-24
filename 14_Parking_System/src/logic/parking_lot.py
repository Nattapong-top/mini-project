import math
from datetime import datetime

class OverLimitError(Exception):
    '''Exception สำหรับกรณีจออดรถเกินเวลาที่กำหนด'''
    pass

class ParkingFullError(Exception):
    '''Exception เมื่อที่จอดรถเต็ม'''
    pass

class ParkingLot:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.parked_vehicles = []
        self.hourly_rate = 20
        self.hour_limit = 24
        self.max_daily_fee = 200
        self.lost_ticket_penalty = 100
    
    def get_available_slots(self):
        '''คืนค่าจำนวนที่วางที่เหลืออยู่'''
        return self.capacity - len(self.parked_vehicles)
    
    def check_in(self, license_plate):
        '''รับรถเข้าจอด'''
        # กฎเหล็ก ถ้าที่ว่างไม่เหลือแล้ว (เป็น 0 หรือน้อยกว่า) ให้แจ้ง
        if self.get_available_slots() <= 0:
            raise  ParkingFullError('ที่จอดรถเต็มแล้ว')
        
        # ถ้ามีที่ว่าง ก็เพิ่มเข้าไปใน list
        self.parked_vehicles.append(license_plate)
        return True

    # def test_


    def validate_duration(self, hours):
        if hours > self.hour_limit:
            raise OverLimitError('จอดเกิน 24 ชั่งโมง ต้องติดต่อพนักงาน')

    def calculate_fee(self, entry_time_str, exit_time_str=None, is_lost=False):
        # แปลงข้อความเวลาเป็น Object ของ Python
        entry_time = datetime.strptime(entry_time_str, '%Y-%m-%d %H:%M:%S')

        if exit_time_str:
            exit_time = datetime.strptime(exit_time_str, '%Y-%m-%d %H:%M:%S')
        else:
            exit_time = datetime.now()

        duration = exit_time - entry_time
        
        # ปัดเศษชั่วโมงขึ้น
        total_seconds = duration.total_seconds()
        hours = math.ceil(total_seconds / 3600)

        # ถ้าจอดนานเกิน 24 ชั่วโมง ติดต่อพนักงาน
        self.validate_duration(hours)

        actual_fee = 0
        # 1. ลอจิกปกติ: 2 ชม. แรกฟรี
        if hours > 2:
            actual_fee = (hours - 2) * self.hourly_rate
        
        # 2. ลอจิกเพดานราคา: ไม่เกิน 200
        if actual_fee > self.max_daily_fee:
            actual_fee = self.max_daily_fee

        # 3. ลอจิกระดับเซียนของป๋า: ถ้าบัตรหาย ถ้าน้อยกว่า 100 คิด 100
        if is_lost:
            return max(self.lost_ticket_penalty, actual_fee)
        
        return actual_fee