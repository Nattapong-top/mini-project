import pytest
from datetime import datetime
from domain.models import ParkingTicket, LicensePlate
from adapters.sqlite_repository import SqliteParkingRepository

def test_repository_can_save_and_retrieve_a_ticket():
    # 1. Arrange (เตรียมของ)
    # ต้องเริ่มสร้าง Value Object และ Entiry ก่อน
    repo = SqliteParkingRepository(':memory:')
    repo.create_tables() #ต้องมีคำสั่ง สร้าง tables ด้วย

    plate = LicensePlate('กข-1234')
    entry_now = datetime.now()
    ticket = ParkingTicket(license_plate=plate, entry_time=entry_now)

    # 2. Act (สั่งรันสิ่งที่อยากทดสอบ)
    repo.seve(ticket)
    retrieved_ticket = repo.get_by_plate(plate)

    # 3. Assert (ตรวจสอบผลลัพธ์)
    assert retrieved_ticket is not None
    assert retrieved_ticket.license_plate.value == 'กข-1234'
    assert retrieved_ticket.version == 1
    # ตรวจสอบเวลา (ต้องระวังเรื่อง format เวลาตอนเก็บใน sql เล็กน้อย)
    assert retrieved_ticket.entry_time.isoformat() == entry_now.isoformat()