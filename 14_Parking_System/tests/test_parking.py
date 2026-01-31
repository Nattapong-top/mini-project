import pytest
from datetime import datetime, timedelta
from domain.models import (
    ParkingTicket, 
    LicensePlate, 
    PricingPolicy, 
    OverLimitError)

def test_parking_ticket_calculate_fee_correctly():
    # Arrange: รถเข้าจอดเมื่อ 3 ชม. ที่แล้ว (ชั่วโมงละ 20 บาท)
    my_policy = PricingPolicy(hourly_rate=20)
    plate = LicensePlate(value='กข-1234')
    fixed_now = datetime.now()
    entry_now = fixed_now - timedelta(hours=3)
    ticket = ParkingTicket(license_plate=plate, entry_time=entry_now)

    # Act: คำนวณค่าธรรมเนียม ฟรี สองชั่งโมงแรก
    # สมมุติค่าจอดรถ: 3 - 2 ชม. x 20 บาท = 20
    fee = ticket.calculate_fee(current_time=fixed_now, Policy=my_policy)

    # 3. Assert (ตรวจสอบผลลัพธ์)
    assert fee == 20

def test_parking_under_2_hours_is_free():
    # จอด 1 ชม. 30 นาที (ต้องปัดเป็น 2 ชม. และต้องฟรี)
    my_policy = PricingPolicy(hourly_rate=20)
    fixed_now = datetime.now()
    entry_time = fixed_now - timedelta(hours=1, minutes=30)
    ticket = ParkingTicket(license_plate=LicensePlate(value='ป๋า-9999'), entry_time=entry_time)

    fee = ticket.calculate_fee(current_time=fixed_now, Policy=my_policy)

    assert fee == 0

def test_parking_over_24_hour_should_raise_error():
    my_policy = PricingPolicy(hour_limit=24)
    fixed_now = datetime.now()
    entry_time = fixed_now - timedelta(hours=24, minutes=30)
    ticket = ParkingTicket(license_plate=LicensePlate(value='ป๋า-9999'), entry_time=entry_time)

    # ใช้ pytest.raises เพื่อดักรอ Error
    with pytest.raises(OverLimitError) as excinfo:
        ticket.calculate_fee(current_time=fixed_now, Policy=my_policy)

    # ตรวจสอบว่าข้อความใน Error ตรงกับที่เราตั้งใจไว้ไหม
    assert str(excinfo.value) == 'จอดเกินเวลา กรุณาติดต่อพนักงาน'