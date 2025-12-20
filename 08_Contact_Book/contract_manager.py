'''Project 8: สมุดโทรศัพท์ (Contact Book)
เป้าหมาย: สร้างสมุดโทรศัพท์ที่เก็บ ชื่อ, เบอร์โทร, อีเมล และแยกการทำงานเป็นสัดส่วน'''

import os

# 
script_dir = os.path.dirname(__file__)
filename = os.path.join(script_dir, 'contract.txt')

def load_contracts():
    '''อ่านรายชื่อทั้งหมดจากไฟล์'''
    contract = []
    if os.path.exists(filename):
        with open(filename, encoding='utf-8') as f:
            for line in f:
                # รูปแบบ: ชื่อ,เบอร์โทร,อีเมล
                parts = line.strip().split(',')
                # เช็คก่อนว่าตรงตามรูปแบบไหม
                if len(parts) == 3:
                    contract.append(parts)
    return contract



