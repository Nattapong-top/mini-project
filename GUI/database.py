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

def add_invoice(invoice_obj: Invoice):
    """
    ฟังก์ชันสำหรับ 'เพิ่ม' ข้อมูล 1 รายการลงในฐานข้อมูล
    รับ 'object' จาก class Invoice เข้ามา 
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # เราจะดึงข้อมูลจาก object ที่คำนวณเสร็จแล้ว
        data_to_insert = (
            invoice_obj.tenant_name,
            invoice_obj.room_number,
            invoice_obj.invoice_date.isoformat(), # แปลงวันที่เป็น string
            invoice_obj.water_units,
            invoice_obj.electric_units,
            invoice_obj.water_cost,
            invoice_obj.electric_cost,
            invoice_obj.grand_total
        )

        # ใช้ "?" (placeholders) เพื่อป้องกัน SQL Injection
        sql = """
        INSERT INTO invoines
        (tenant_name, room_number, invoice_date, water_units,
        electric_units, water_cost, electric_cost, grand_total)        
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(sql, data_to_insert)
        conn.commit()
        conn.close()
        print(f'บันทึกบิลของ {invoice_obj.tenant_name} เรียร้อย')
        return True # คือค่าว่า สำเร็จ
    
    except sqlite3.Error as e:
        print(f'เกิดข้อผิดลาดขณะบันทึก: {e}')
        return False # คืนค่าว่าล้มเหลว