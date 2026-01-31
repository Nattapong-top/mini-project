import datetime
from domain.barrier_interfaces import BarrierInterface
from domain.models import LicensePlate, ParkingTicket

# domain/services.py
class ParkingRegistrationService:
    def __init__(self, barrier: BarrierInterface):
        self.barrier = barrier  # รับพนักงานเข้ามาทำงาน

    def register_entry(self, license_plate: LicensePlate, entry_time: datetime):
        # ... logic การสร้าง Ticket ของป๋า ...
        ticket = ParkingTicket(license_plate=license_plate, entry_time=entry_time)
        
        # --- นี่คือส่วนที่ป๋าต้องเพิ่ม ---
        self.barrier.open() 
        # ---------------------------
        
        return ticket