import sqlite3

class SqliteRepository:
    def __init__(self, db_path='/14_Parking_System/data/parking_system.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()


    def create_tables(self, ):
        self.cursor = self.conn.cursor()
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS active_parking (
                       license_plate TEXT PRIMARY KEY,
                       entry_time TEXT NOT NULL
            )
        ''')
        self.conn.commit()
    
    def save_vehicle_in_parking(self, license_plate, entry_time):
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO active_parking VALUES (?, ?)', (license_plate, entry_time))
        self.conn.commit()
    
    def show_all_vehicle_in_parking(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM active_parking')
        return {row[0]: row[1] for row in cursor.fetchall()}
    
    def remove_vehicle_in_parking(self, license_plate):
        cursor = self.conn.cursor()

        # คำสั่ง sql ลบข้อมูล
        query = 'DELETE FROM active_parking WHERE license_plate = ?'

        # สั่งรันคำสั่ง sql พร้อมส่งตัวแทนเข้าไปแทนที่ ?
        cursor.execute(query, (license_plate,))
        self.conn.commit()

    def check_vehicle_in_parking(self, license_plate):
        cursor = self.conn.cursor()

        query = 'SELECT license_plate FROM active_parking WHERE license_plate = ?'
        cursor.execute(query, (license_plate,))
        result = cursor.fetchone()

        if result:
            return result[0]
        return None
    
    def count_all_vehicle_in_parking(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT (license_plate) FROM active_parking')
        count = cursor.fetchone()

        if count:
            return count[0]
        return 0