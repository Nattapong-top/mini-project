from datetime import datetime, timedelta
from domain.value_objects import LicensePlate, MoneyThb
from domain.models import ParkingTicket
from domain.services import ParkingRegistrationService
from domain.barrier_spay import BarrierSpy
from adapters.InMemoryParkingRepository import InMemoryParkingRepository


def test_payment_success_opens_barrier(fixed_now, standard_policy):
    # Arrange
    spy_barrier = BarrierSpy()
    repo = InMemoryParkingRepository() # ใช้ตัวปลอมในแรมจะได้เร็วๆ
    service = ParkingRegistrationService(spy_barrier, repo, standard_policy)
    
    # เอารถเข้าจอดก่อน (3 ชั่วโมง)
    entry_time = fixed_now - timedelta(hours=2, minutes=59)
    ticket = ParkingTicket(license_plate=LicensePlate(value='รวย-999'), entry_time=entry_time)
    repo.save(ticket)

    # Act: จ่ายเงิน 20 บาท (จอด 3 ชม. ฟรี 2 ชม. เหลือจ่าย 1 ชม. = 20 บาท)
    fee = ticket.calculate_fee(fixed_now, standard_policy)
    payment = MoneyThb(value=20)
    
    print(f"\n--- ป๋าดูนี่! Fee: {fee.value}, Payment: {payment.value} ---")

    service.process_payment(LicensePlate(value='รวย-999'), payment, fixed_now)

    # Assert
    assert spy_barrier.is_open is True
    assert repo.get_by_plate(LicensePlate(value='รวย-999')).is_paid is True