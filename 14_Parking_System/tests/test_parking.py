import pytest
from datetime import datetime, timedelta
from domain.models import ParkingTicket, LicensePlate, PricingPolicy

def test_parking_ticket_calculate_fee_correctly():
    # Arrange: รถเข้าจอดเมื่อ 3 ชม. ที่แล้ว (ชั่วโมงละ 40 บาท)
    my_policy = PricingPolicy(hourly_rate=40)
    plate = LicensePlate(value='กข-1234')
    fixed_now = datetime.now()
    entry_now = fixed_now - timedelta(hours=3)
    ticket = ParkingTicket(license_plate=plate, entry_time=entry_now)

    # Act: คำนวณค่าธรรมเนียม
    # สมมุติค่าจอดรถ: 3 ชม. x 40 บาท = 120
    fee = ticket.calculate_fee(current_time=fixed_now, Policy=my_policy)

    # 3. Assert (ตรวจสอบผลลัพธ์)
    assert fee == 40

def test_parking_under_2_hours_is_free():
    # จอด 1 ชม. 30 นาที (ต้องปัดเป็น 2 ชม. และต้องฟรี)
    my_policy = PricingPolicy(hourly_rate=40)
    fixed_now = datetime.now()
    entry_time = fixed_now - timedelta(hours=1, minutes=30)
    ticket = ParkingTicket(license_plate=LicensePlate(value='ป๋า-9999'), entry_time=entry_time)

    fee = ticket.calculate_fee(current_time=fixed_now, Policy=my_policy)

    assert fee == 0