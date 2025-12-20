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

def save_contracts(contracts:list):
    '''บันทึกข้อมูลทับลงไฟล์'''
    with open(filename, 'w', encoding='utf-8') as f:
        for item in contracts:
            line = ','.join(item)
            f.write(line + '\n')
    print('💾 บันทึกข้อมูลเรียบร้อย!')

def show_all_contracts(contracts:list):
    '''แสดงรายชื่อแบบตาราง'''
    print('\n' + '='*60)
    print(f"{'ชื่อ':<20} {'เบอร์โทร':<15} {'อีเมล':<20}")
    print('='*60)

    if not contracts:
        print(" (สมุดโทรศัพท์ว่างเปล่า)")
    else:
        for i, item in enumerate(contracts):
            # i=No. item[0]=ชื่อ, item[1]=เบอร์โทร, item[2]=email
            print(f'{i+1:<2} {item[0]:<20} {item[1]:<15} {item[2]:<20}')
            print('='*60)

