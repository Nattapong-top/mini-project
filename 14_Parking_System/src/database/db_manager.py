import sqlite3
import os

class DBManager:
    def __init__(self, db_path='/14_Parking_System/data/parking_system.db'):
        # ตรวจสอบว่าโฟลเดอร์ data มีอยู่หรือไม่ ถ้าไม่มีก็สร้างขึ้นมา
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        # เชื่อมต่อกับฐานข้อมูล SQLite
        self.conn = sqlite3.connect(db_path)
        
        # สร้าง cursor
        self.cursor = self.conn.cursor()

        # สร้างตารางถ้ายังไม่มี
        self.create_tables()


    def create_tables(self):
        ''' สร้างตารางตามที่ออกแบบไว้ '''        
        # ตารางรถ
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicles (
                vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_card TEXT NOT NULL,
                license_plate TEXT UNIQUE,
                owner_name TEXT NOT NULL
            )
        ''')
        # ตารางที่จอดรถ
        self.cursor.execute('''
            create table if not exists ParkingRecords (
                ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_id INTEGER,
                entry_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                exit_time DATETIME,
                fee REAL DEFAULT 0,
                status TEXT DEFAULT 'IN',
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
            )
        ''')
    def add_record(self, license_plate, id_card, owner_name):
        """ฟังก์ชันจดบันทึกข้อมูลรถเข้าลงฐานข้อมูล"""

        # 1. บันทึกข้อมูลรถ (ถ้าทะเบียนซ้ำ ให้ขยับไปอัปเดตชื่อและเลขบัตรแทน)
        self.cursor.execute(
            """
            INSERT INTO vehicles (license_plate, id_card, owner_name) 
            VALUES (?, ?, ?)
            ON CONFLICT(license_plate) DO UPDATE SET
                id_card = excluded.id_card,
                owner_name = excluded.owner_name
            """,
            (license_plate, id_card, owner_name)
        )

        # 2. ดึงรหัสรถ (vehicle_id) มาเพื่อใช้เชื่อมโยงข้อมูล
        self.cursor.execute("SELECT vehicle_id FROM Vehicles WHERE license_plate = ?", (license_plate,))
        vehicle_id = self.cursor.fetchone()[0]

        # 3. บันทึกประวัติการจอดใหม่ลงตาราง ParkingRecords (เวลาเข้าจะบันทึกอัตโนมัติ)
        self.cursor.execute(
            "INSERT INTO ParkingRecords (vehicle_id, status) VALUES (?, 'IN')",
            (vehicle_id,)
        )

        self.conn.commit()
    
    def close(self):
        self.conn.close()