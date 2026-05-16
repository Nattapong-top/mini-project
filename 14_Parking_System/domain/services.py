from datetime import datetime
from typing import Tuple

from .models import ParkingTicket, PricingPolicy
from .value_objects import MoneyThb, LicensePlate
from adapters.repository_interface import ParkingRepository
from .barrier_interfaces import BarrierInterface
from .exceptions import InsufficientPaymentError


class ParkingRegistrationService:
    def __init__(
        self, 
        barrier: BarrierInterface, 
        repository: ParkingRepository, 
        policy: PricingPolicy
    ):
        """
        Dependency Injection: ป๋าส่งอาวุธมาให้ครบมือ ทั้งไม้กั้น โกดัง และนโยบายราคา
        """
        self.barrier = barrier
        self.repository = repository
        self.policy = policy

    def register_entry(self, license_plate: LicensePlate, entry_time: datetime) -> ParkingTicket:
        """
        จังหวะรถเข้า: สร้างตั๋ว -> บันทึก -> เปิดไม้กั้น
        """
        # 1. สร้างตั๋วใบใหม่ (Domain Entity)
        ticket = ParkingTicket(license_plate=license_plate, entry_time=entry_time)
        
        # 2. สั่งโกดังให้บันทึกข้อมูล (Optimistic Locking จะทำงานในระดับ Repository)
        self.repository.save(ticket)
        
        # 3. สั่งเปิดไม้กั้น
        self.barrier.open()
        
        print(f"--- ป๋าครับ! รถทะเบียน {license_plate.value} เข้าจอดเรียบร้อย ---")
        return ticket

    def check_out(self, ticket: ParkingTicket, payment: MoneyThb, fee: MoneyThb):
            """รถออก (ตัวที่ป๋าตามหา): เช็คเงิน -> เปิดไม้กั้น"""
            # ใช้ความฉลาดของ MoneyThb ที่ป๋าทำไว้
            if payment < fee:
                # จ่ายไม่ครบ ไม่เปิดไม้กั้น และคืน False
                return False
                
            self.barrier.open()
            return True

    def process_payment(
        self, 
        plate: LicensePlate, 
        payment: MoneyThb, 
        current_time: datetime
    ) -> Tuple[ParkingTicket, MoneyThb]:
        """
        จังหวะรถออก: ดึงตั๋ว -> คำนวณเงิน -> เช็คยอด -> เปิดไม้กั้น
        """
        # 1. ดึงข้อมูลจากโกดัง (ถ้าไม่เจอต้องด่า เอ้ย! ต้องบอกป๋าครับ)
        ticket = self.repository.get_by_plate(plate)
        if not ticket:
            raise ValueError(f"ไม่พบรถทะเบียน {plate.value} ในระบบครับป๋า")

        # 2. ให้ Entity คำนวณค่าธรรมเนียมตาม Policy (Logic อยู่ใน Entity ตามกฎป๋าเป๊ะ)
        fee = ticket.calculate_fee(current_time, self.policy)

        # 3. ตรวจสอบยอดเงิน (Business Rule: จ่ายไม่ครบ ห้ามออก!)
        # ใช้ความฉลาดของ MoneyThb ที่ป๋าทำ Operator Overloading ไว้ (payment >= fee)
        if payment < fee:
            raise InsufficientPaymentError(
                f"ป๋าครับ! เงินไม่พอ ยอดต้องจ่าย {fee.value} แต่จ่ายมา {payment.value}"
            )
        
        # --- จ่ายเงินครบแล้ว ลบออกจากตาราง Active เลยครับป๋า ---
        self.repository.remove(plate)
        
        # --- ส่วนที่ต้องเพิ่ม: บันทึกสถานะลงสมุดบัญชี ---
        ticket.is_paid = True
        ticket.paid_amount = payment
        ticket.exit_time = current_time
        
        # สำคัญมาก: ต้องสั่งเซฟกลับไปที่ Repo ด้วย!
        # (นี่แหละครับที่ Optimistic Locking จะช่วยเช็คว่ามีใครมาแก้ตัดหน้าไหม)
        # self.repository.save(ticket)
        
        # 4. เปิดไม้กั้น
        self.barrier.open()
        
        print(f"--- ป๋าครับ! รถทะเบียน {plate.value} จ่ายเงินครบ {payment.value} บาท ขับออกได้เลย ---")
        return ticket, fee