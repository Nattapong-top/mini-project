from domain.repository_interface import ParkingRepository
from domain.models import ParkingTicket, LicensePlate
from datetime import datetime
import sqlite3

class SqliteParkingRepository(ParkingRepository):
    def __init__(self, db_path='/14_Parking_System/data/parking_system.db'):
        self.conn = sqlite3.connect(db_path)

    def create_tables(self):
        cursor = self.conn.cursor()
        # เพิ่ม field 'version' กันการแก้ไขซ้ำกัน
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS active_parking (
                    license_plate  TEXT PRIMARY KEY,
                    entry_time TEXT NOT NULL,
                    version INTEGER NOT NULL DEFAULT 1
            )
        ''')
        self.conn.commit()

    def save(self, ticket: ParkingTicket):
        cursor = self.conn.cursor()
        # แปลง Onject กลับเป็น data เพื่อลง DB
        plate_str = ticket.license_plate.value
        time_str = ticket.entry_time.isoformat()

        # ใช้ Optimistic Locking ตรงนี้!
        # ถ้าพยายาม Update แต่ version ไม่ตรงกัน มันจะไม่ยอดให้อัพเดท 
        cursor.execute('''
            INSERT INTO active_parking (license_plate, entry_time, version)
            VALUES (?, ?, ?)
            ON CONFLICT(license_plate) DO UPDATE SET 
                entry_time=excluded.entry_time, 
                version=active_parking.version + 1
            WHERE active_parking.version = ?
        ''', (plate_str, time_str, ticket.version, ticket.version))
        self.conn.commit()
        
    def get_by_plate(self, plate: LicensePlate) -> ParkingTicket:
        cursor = self.conn.cursor()
        cursor.execute('SELECT license_plate, entry_time, version FROM active_parking' \
                            ' WHERE license_plate = ?', (plate.value,))
        row = cursor.fetchone()

        if row:
            # ประกอบร่างข้อมูล (Reconstitute) ข้อมูลจาก DB กลับมาเป็น Object
            return ParkingTicket(
                license_plate=LicensePlate(value=row[0]),
                entry_time=datetime.fromisoformat(row[1]),
                version=row[2]
            )
        return None
    