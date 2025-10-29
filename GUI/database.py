import sqlite3
import datetime
from Invoice import Invoice # import class Invoice มาเพื่อ type hint

# ชื่อไฟล์ฐานข้อมูล
DB_FILE = 'billing_records.db'

def init_db():
    '''ฟังก์ชันสร้างไฟล์ฐานข้อมูล .db และสร้างตาราง (Table) ถ้ายังไม่มี '''
    