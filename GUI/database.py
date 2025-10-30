import sqlite3
import datetime
from Invoice import Invoice # import class Invoice มาเพื่อ type hint

# ชื่อไฟล์ฐานข้อมูล
DB_FILE = 'billing_records.db'

def init_db():
    '''ฟังก์ชันสร้างไฟล์ฐานข้อมูล .db และสร้างตาราง (Table) ถ้ายังไม่มี '''
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # สร้างตารางชื่อ 'invoices'
        # เก็บข้อมูลสำคัญไว้ใน database 
        cursor.execute("""
        CREATE TABALE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_name TEXT NOT NULL,
            room_number TEXT,
            invoice_date TEXT NOT NULL,
            water_units INTEGER,
            electric_units INTEGER,
            water_cost REAL,
            electric_cost REAL,
            grand_total REAL NOT NULL
        )
        """)

        conn.commit()
        conn.close()
        print("ฐานข้อมูล '{DB_FILE}' พร้อมใช้งาน")

    except sqlite3.Error as e:
        print(f'เกิดข้อผิดพลาดกับฐานข้อมูล: {e}')

def 

