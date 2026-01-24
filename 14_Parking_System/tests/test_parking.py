import unittest
from datetime import datetime, timedelta
from src.logic.parking_lot import ParkingLot, OverLimitError


class TestParkingLogic(unittest.TestCase):
    def test_calculate_fee_within_free_time(self):
        logic = ParkingLot()
        # ทดสอบเข้า 10 ออก 11:30 ไม่ถึง 2 ชั่งโมง
        # ผลลัพธ์ที่คาดหวัง คือ 0 บาท
        entry = '2026-01-24 10:00:00'
        exit_time = '2026-01-24 12:00:00'
        fee = logic.calculate_fee(entry_time_str=entry, exit_time_str=exit_time) 
        self.assertEqual(fee, 0)

    def test_calculate_fee_over_free_time(self):
        logic = ParkingLot()
        # ทดสอบจอด 3 ชั่วโมง
        # ผลลัพธ์ที่คาดหวัง คือ (3-2) * 20 = 20 บาท
        entry = '2026-01-24 10:00:00'
        exit_time = '2026-01-24 13:00:00'
        fee = logic.calculate_fee(entry_time_str=entry, exit_time_str=exit_time)
        self.assertEqual(fee, 20)

    def test_calculate_over_limit_fee(self):
        logic = ParkingLot()
        # ทดสอบจอด 3 ชั่วโมง
        # ผลลัพธ์ที่คาดหวัง คือ (3-2) * 20 = 20 บาท
        entry = '2026-01-24 00:00:00'
        exit_time = '2026-01-24 12:00:00'
        fee = logic.calculate_fee(entry_time_str=entry, exit_time_str=exit_time)
        self.assertEqual(fee, 200)

    def test_calculate_over_limit_24_hores(self):
        logic = ParkingLot()
        entry = '2026-01-23 00:00:00'
        exit_time = '2026-01-24 12:00:00'

        # ตรวจสอบว่าแจ้ง Error ออกมาเมื่อจอดเจอเวลาหรือไม่
        with self.assertRaises(OverLimitError):

            logic.calculate_fee(entry_time_str=entry, exit_time_str=exit_time)


