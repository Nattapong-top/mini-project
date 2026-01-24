from database.db_manager import DBManager
from logic.parking_lot import ParkingLot

def main():
    # ทดสอบสร้าง Database
    db = DBManager()
    
    # ทดสอบเรียกใช้ Logic การคำนวณ
    logic = ParkingLot()
    db.add_record("กก-1234", "1100112233445", 'นาย นนทพัฒ สำราญรมณ์')
    # สมมติสถานการณ์: จอดรถ 5 ชม. (เกินฟรี 2 ชม.)
    # เวลาเข้าสมมติ (3 ชั่วโมงที่แล้ว)
    fake_entry = "2026-01-24 10:00:00" 
    fee = logic.calculate_fee(fake_entry, is_lost=False)
    
    print(f"--- ทดสอบระบบ ---")
    print(f"ค่าจอดรถปกติ: {fee} บาท")
    print(f"ค่าจอดกรณีบัตรหาย: {logic.calculate_fee(fake_entry, is_lost=True)} บาท")

if __name__ == "__main__":
    main()