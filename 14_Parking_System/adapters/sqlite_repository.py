import sqlite3

class SqliteParkingRepository(ParkingRepository):
    def __init__(self, db_path='/14_Parking_System/data/parking_system.db'):
        self.conn = sqlite3.connect(db_path)


    def seve(self, ticket: ParkingTicket):
        cursor = self.conn.cursor()
        # แปลง Onject กลับเป็น data เพื่อลง DB
        plate_str = ticket.license_plate.value
        time_str = ticket.entry_time.isformat()

        # ใช้ Optimistic Locking ตรงนี้!
        # ถ้าพยายาม Update แต่ version ไม่ตรงกัน มันจะไม่ยอดให้อัพเดท 
        cursor.execute('''
            INSERT INTO active_parking (license_plate, entry_time, version)
            VALUES (?, ?. ?)
            ON CONFLICT(license_plate) DO UPDATE SET 
                entry_time=excluded.entry_time, 
                version=active_parking.version + 1
            WHERE active_parking.version = ?
        ''', (plate_str, time_str, ticket.version))
        self.conn.commit()
        