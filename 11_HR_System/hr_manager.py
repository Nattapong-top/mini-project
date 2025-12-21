'''🧠 Logic การคำนวณ (Business Logic)
เพื่อให้สมจริง (แบบย่อ) เราจะใช้กติกานี้ครับ:
ประกันสังคม (SSO): หัก 5% ของเงินเดือน (แต่สูงสุดไม่เกิน 750 บาท)
ภาษี (Tax): คิดแบบขั้นบันไดง่ายๆ
เงินเดือนไม่เกิน 20,000 = ไม่เสียภาษี
เกิน 20,000 = หัก 3%
เกิน 50,000 = หัก 5% (คนรวยจ่ายเยอะหน่อย)
เงินสุทธิ (Net Salary): เงินเดือน - ประกันสังคม - ภาษี'''

import os


script_dir = os.path.dirname(__file__)
filename = os.path.join(script_dir, 'employees.txt')

def load_employees():
    '''อ่านข้อมูลพนักงาน: รหัส, ชื่อ, เงินเดือน, ตำแหน่ง'''
    employees = []
    if os.path.exists(filename):
        with open(filename, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                employees.append(parts)
    return employees

def save_employees(employees:list):
    '''บันทึกข้อมูลใน list เข้าไปเก็บไว้ใน file'''
    with open(filename, 'w', encoding='utf-8') as f:
        for item in employees:
            line = ','.join(item)
            f.write(line + '\n')
    print('💾 บันทึกข้อเรียบร้อย!')

def add_employee(employees:list):
    print('\n --- ➕ เพิ่มพนักงานใหม่ ---')
    emp_id = input('รหัสพนักงาน (EMP01): ').strip().upper()

    for item in employees:
        if item[0] == emp_id:
            print('❌ รหัสนี้มีอยู่แล้ว')
            return

    name = input('ชื่อ-นามสกุล: ').strip()

    while True:
        sarary_str = input('เงินเดือน (บาท): ').strip()
        if sarary_str.isdigit():
            break
        print('❌ ใส่ตัวเลขเท่านั้นครับ!')
    
    position = input('ตำแหน่งงาน: ').strip()

    # เก็บ List (salary เก็บเป็น str ไปก่อนเพือนให้ save ง่าย)
    employees.append([emp_id, name, sarary_str, position])
    save_employees(employees)
    print(f'✅ ยินดีต้อนรับคุณ {name} สู่ทีม')

def delete_employee(employees:list):
    print('\n---🗑️ ลบข้อมูลพนักงาน ---')
    target_id = input('ป้อนรหัสพนักงานที่จะลบ: ').strip().upepr()

    found = False
    for item in employees:
        if item[0] == target_id:
            print(f'เจอคุณ: {item[1]} (ตำแหน่ง: {item[3]})')
            confirm = input('ยืนยันการลาออก (y/n): ').lower()
            if confirm == 'y':
                employees.remove(item)
                found = True
                print('✅ ลบเรียบร้อย')
                break
            else:
                return
    
    if found:
        save_employees(employees)
    else:
        print('❌ ไม่พบรหัสนี้')
