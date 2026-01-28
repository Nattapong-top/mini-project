import math
from datetime import datetime

class OverLimitError(Exception):
    '''Exception สำหรับกรณีจออดรถเกินเวลาที่กำหนด'''
    pass

class ParkingFullError(Exception):
    '''Exception เมื่อที่จอดรถเต็ม'''
    pass

class TimeService:
    '''Class กลางสำหรับจัดการเรื่องเวลา (Time Utility)'''
    FORMAT = '%Y-%m-%d %H:%M:%S'

    @staticmethod
    def get_now_str():
        '''ดึงเวลาปัจจุบันในรูปแบบข้อความ'''
        return datetime.now().strftime(TimeService.FORMAT)

    @staticmethod
    def calculate_hours(entry_time_str, exit_time_str=None):
        '''คำนวณชั่วโมงระหว่างเวลาเข้าและออก'''
        entry_time = datetime.strptime(entry_time_str, TimeService.FORMAT)

        if exit_time_str:
            exit_time = datetime.strptime(exit_time_str, TimeService.FORMAT)
        else:
            exit_time = datetime.now()

        duration = exit_time - entry_time
        total_seconds = duration.total_seconds()

        # ปัดเศษชั่วโมงขึ้น (1 นาที ก็นับเป็น 1 ชม.)
        hours = math.ceil(total_seconds / 3600)
        return hours


class ParkingLot:
    def __init__(self, capacity=10, repository=None):
        self.capacity = capacity
        self.repository = repository
        self.parked_vehicles = {}
        self.hourly_rate = 20
        self.hour_limit = 24
        self.max_daily_fee = 200
        self.lost_ticket_penalty = 100
        self.is_barrier_open = False
        self.parked_vehicles = self.repository.load_all() if repository else {}
    
    def get_available_slots(self):
        '''คืนค่าจำนวนที่วางที่เหลืออยู่'''
        return self.capacity - len(self.parked_vehicles)
    
    def check_in(self, license_plate, entry_time=None):
        '''รับรถเข้าจอด'''
        # กฎเหล็ก ถ้าที่ว่างไม่เหลือแล้ว (เป็น 0 หรือน้อยกว่า) ให้แจ้ง
        if self.get_available_slots() <= 0:
            raise  ParkingFullError('ที่จอดรถเต็มแล้ว')
        
        # กรณีรถไม่มีทะเบียน ให้สร้าง ID พิเศษขึ้นมาแทน
        actual_plate = license_plate
        if not license_plate or license_plate.strip() == '':
            actual_plate = self._generate_temp_id() # คอลสร้าง id ชั่วคราว
            print(f'>>> [SYSTEM] รถไม่มีทะเบียน! ออกรหัสชั่วคราว')
        

        # ถ้ามีที่ว่าง ก็เพิ่มเข้าไปใน list
        self.parked_vehicles[actual_plate] = entry_time if entry_time else TimeService.get_now_str()
        self.open_barrier() # เปิดไม้กั้นขึ้น
        return actual_plate
    
    def _generate_temp_id(self):
        # สร้าง ID TEMP ให้กับรถไม่มีทะเบียน
        return f'TEMP-{TimeService.get_now_str()}'
 

    def check_out(self, license_plate, exit_time=None, is_lost=False):
        # เช็คว่ามีรถในระบบไหม
        if license_plate not in self.parked_vehicles:
            raise ValueError('ไม่พบทะเบียนรถนี้ในระบบ')

        # ดึงเวลาเข้าที่ระบบจำไว้ (ไม่ต้องกรอกเองแล้ว)
        entry_time = self.parked_vehicles[license_plate]

        # คำนวณชั่งโมง เวลาเข้า เวลาออก รวมกี่ชั่วโมง
        hours = TimeService.calculate_hours(entry_time, exit_time)

        # ถ้าจอดนานเกิน 24 ชั่วโมง ติดต่อพนักงาน
        self.validate_duration(hours)

        # คำนวณเงิน
        fee = self.calculate_fee(hours, is_lost)

        # สมมติว่ากระบวนการจ่ายเงินเสร็จสิ้นในฟังก์ชันนี้
        print(f">>> [SYSTEM] รับเงิน {fee} บาท เรียบร้อย")

        # คืนที่ว่างที่จอดรถ
        del self.parked_vehicles[license_plate]
        self.open_barrier()     # เปิดไม้กั้นเพื่อให้รถออก
        return fee

    def validate_duration(self, hours):
        if hours > self.hour_limit:
            raise OverLimitError('จอดเกิน 24 ชั่งโมง ต้องติดต่อพนักงาน')

    def calculate_fee(self, hours, is_lost=False):
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
    
    def close_barrier(self):
        '''สั่งไม้้กั้นลง'''
        print('>>> [SYSTEM] ไม้กั้นกำลังปิดลง...')
        self.is_barrier_open = False

    def open_barrier(self):
        '''สั้งไม้กั้นขึ้น'''
        print('>>> [SYSTEM] ไม้กั้นกำลังเปิดขึ้น...')
        self.is_barrier_open = True
    
    def vehicle_passed(self):
        '''เหตุการณ์เมื่อรถผ่านเซนเซอร์หลังไม้กั้น'''
        self.close_barrier()

    