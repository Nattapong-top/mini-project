import pytest
from datetime import datetime, timedelta
from domain.models import ParkingTicket
from domain.value_objects import LicensePlate
from domain.exceptions import ConcurrencyError,OverLimitError, InsufficientPaymentError
from domain.repository_interface import ParkingRepository
from domain.services import ParkingRegistrationService
from adapters.sqlite_repository import SqliteParkingRepository


def test_optimistic_locking_prevents_data_overwrite():
    # 1. Arrange: เตรียมสนามสอบ
    # ใช้ ":memory:" เพื่อให้ SQLite สร้าง DB ในแรม (รันเสร็จหายไป ไม่รกเครื่อง)
    repo = SqliteParkingRepository(db_path=":memory:") 
    repo.create_tables()
    
    lp = LicensePlate(value='รวย-888')
    entry_time = datetime.now()
    
    # บันทึกรถเข้าครั้งแรก (Version 1)
    initial_ticket = ParkingTicket(license_plate=lp, entry_time=entry_time, version=1)
    repo.save(initial_ticket)

    # 2. จำลองพนักงาน 2 คน ดึงข้อมูล Version 1 ไปถือไว้ในมือพร้อมกัน
    paa_a_view = repo.get_by_plate(lp) # ถือบัตร Version 1
    paa_b_view = repo.get_by_plate(lp) # ถือบัตร Version 1 (ข้อมูลชุดเดียวกันเป๊ะ)

    # 3. Act: ป๋า A ทำงานไวกว่า กดบันทึกก่อน
    # ระบบจะเช็ค WHERE version = 1 และอัปเดต DB ให้กลายเป็น Version 2
    repo.save(paa_a_view) 

    # 4. Assert: ป๋า B พยายามจะบันทึกตาม (แต่ในมือยังถือ Version 1 อยู่)
    # เราคาดหวังว่าระบบต้องพ่น ConcurencyError ออกมาขวางไว้!
    with pytest.raises(ConcurrencyError) as excinfo:
        repo.save(paa_b_view)

    # เช็คข้อความ Error ให้ชัวร์ว่าใช่เรื่องที่เราตั้งใจไว้ไหม
    assert "ถูกคนอื่นแก้ไขไปแล้ว" in str(excinfo.value)
    print(f"\n--- ป๋าครับ! ระบบป้องกันได้สำเร็จ: {excinfo.value} ---")