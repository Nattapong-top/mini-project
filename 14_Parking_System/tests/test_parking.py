import unittest
from datetime import datetime, timedelta
from src.logic.parking_lot import ParkingLot, OverLimitError, ParkingFullError


class TestParkingLogic(unittest.TestCase):

    def test_barrier_at_check_in(self):
        '''ทดสอบว่าไม้กั้นต้องเปิดเมื่อเช็คอินสำเร็จ'''
        logic = ParkingLot()
        # เริ่มต้นไม้กั้นต้องปิด
        self.assertFalse(logic.is_barrier_open)

        logic.check_in('ป๋า-999')
        # หลังเช็คอินสำเร็จ ไม้กั้นต้องปิด
        self.assertTrue(logic.is_barrier_open)


    def test_barrier_closes_after_vehicle_passed(self):
        '''ทดสอบว่าไม้กั้นต้องลงเมื่อรถผ่านไปแล้ว'''
        logic = ParkingLot()

        logic.check_in('ป๋า-999')

        logic.vehicle_passed() # จำลองเหตุการณ์รถขับผ่านเซนเซอร์
        self.assertFalse(logic.is_barrier_open) # ไม้กั้นต้องปิดลง


    def test_check_out_ticket_lost_higt_fee(self):
        # เทสกรณีบัตรหาย เวลามากว่า 12 ชั่วโมง  = 200
        logic = ParkingLot()
        logic.check_in('กก-4322')
        entry = '2026-01-24 00:00:00'
        exit_time = '2026-01-24 10:00:00'
        fee = logic.check_out('กก-4322', entry, exit_time, is_lost=True)

        self.assertEqual(fee, 160)

    
    def test_check_out_ticket_lost_max_fee(self):
        # เทสกรณีบัตรหาย เวลามากว่า 12 ชั่วโมง  = 200
        logic = ParkingLot()
        logic.check_in('กก-4322')
        entry = '2026-01-24 00:00:00'
        exit_time = '2026-01-24 13:00:00'
        fee = logic.check_out('กก-4322', entry, exit_time, is_lost=True)

        self.assertEqual(fee, 200)


    # เทสกรณีบัตรหาย ไม่เกินเวลา = 100
    def test_check_out_ticket_lost_nomal_100(self):
        logic = ParkingLot()
        logic.check_in('งง-321')
        entry = '2026-01-24 10:00:00'
        exit_time = '2026-01-24 13:00:00'
        fee = logic.check_out('งง-321', entry, exit_time, is_lost=True)

        self.assertEqual(fee, 100)

    def test_check_out_successfully(self):
        logic = ParkingLot(capacity=10)
        # จอดรถออกก่อน 2 ขั่วโมง
        logic.check_in('กข-1234')
        entry = '2026-01-24 10:00:00'
        exit_time = '2026-01-24 13:00:00'
        fee = logic.check_out('กข-1234', entry, exit_time)

        self.assertEqual(fee, 20)
        self.assertEqual(logic.get_available_slots(), 10)


    def test_check_in_vehicle_successfully(self):
        logic = ParkingLot(capacity=2)
        result = logic.check_in('กข-1234')
        self.assertTrue(result)
        self.assertEqual(logic.get_available_slots(), 1)

    def test_check_in_when_full_should_raise_error(self):
        logic = ParkingLot(capacity=1)
        logic.check_in('กข-123')

        # คันที่สองเข้า error 
        with self.assertRaises(ParkingFullError):
            logic.check_in('ขค-5678')

    def test_calculate_fee_within_free_time(self):
        logic = ParkingLot()
        # ทดสอบเข้า 10 ออก 11:30 ไม่ถึง 2 ชั่งโมง
        # ผลลัพธ์ที่คาดหวัง คือ 0 บาท
        entry = '2026-01-24 10:00:00'
        exit_time = '2026-01-24 12:00:00'
        hours = logic.parse_and_calculate_hours(entry, exit_time)
        fee = logic.calculate_fee(hours) 
        self.assertEqual(fee, 0)

    def test_calculate_fee_over_free_time(self):
        logic = ParkingLot()
        # ทดสอบจอด 3 ชั่วโมง
        # ผลลัพธ์ที่คาดหวัง คือ (3-2) * 20 = 20 บาท
        entry = '2026-01-24 10:00:00'
        exit_time = '2026-01-24 13:00:00'
        hours = logic.parse_and_calculate_hours(entry, exit_time)
        fee = logic.calculate_fee(hours)
        self.assertEqual(fee, 20)

    def test_calculate_over_limit_fee(self):
        logic = ParkingLot()
        # ทดสอบจอด 3 ชั่วโมง
        # ผลลัพธ์ที่คาดหวัง คือ (3-2) * 20 = 20 บาท
        entry = '2026-01-24 00:00:00'
        exit_time = '2026-01-24 12:00:00'
        hours = logic.parse_and_calculate_hours(entry_time_str=entry, exit_time_str=exit_time)
        fee = logic.calculate_fee(hours)
        self.assertEqual(fee, 200)

    def test_calculate_over_limit_24_hores(self):
        logic = ParkingLot()
        entry = '2026-01-23 00:00:00'
        exit_time = '2026-01-24 12:00:00'
        hours = logic.parse_and_calculate_hours(entry_time_str=entry, exit_time_str=exit_time)
        
        # ตรวจสอบว่าแจ้ง Error ออกมาเมื่อจอดเจอเวลาหรือไม่
        with self.assertRaises(OverLimitError):

            logic.validate_duration(hours)


