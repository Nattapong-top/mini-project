'''โปรเจคที่ 6 (Boss Level): ระบบทะเบียนคุมทรัพย์สินไอที (Mini IT Asset)
เป้าหมาย: ตรงกับงานจริงของป๋า!
ฟังก์ชัน: รับรหัสครุภัณฑ์, ชื่อ, สถานะ (ปกติ/ส่งซ่อม) -> บันทึกลงไฟล์ -> ค้นหาทรัพย์สินจากรหัส -> แก้ไขสถานะทรัพย์สิน (Update)
สกิลที่ได้: การแก้ไขข้อมูลใน List แล้วบันทึกทับกลับไปในไฟล์ (Update logic)'''

import os

scrip_dir = os.path.dirname(__file__)
filename = os.path.join(scrip_dir, 'assets.txt')

def load_assets():
    '''อ่านไฟล์แล้วคืนค่าเป็น List of Lists'''
    assets = []
    if os.path.exists(filename):
        with open(filename, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 4:
                    assets.append(parts)
    return assets

def save_assets(assets):
    '''รับ List ทั้งหมด แล้วบันทึกทับลงไฟล์ (Mode 'w')'''
    with open(filename, 'w', encoding='utf-8') as f:
        for item in assets:
            # item คือ ['IT-001', 'Notebook', 'Laptop', 'ปกติ']
            # ต้องรวมกลับเป็น string คั่นด้วย comma
            line = ','.join(item)
            f.write(line + '\n')
    print('💾 บันทึกเรียบร้อย!')

def show_all_assets(assets):
    print('\n' + '='*60)
    print(f"{'รหัส':<10} {'ชื่ออุปกรณ์':<25} {'ประเภท':<10} {'สถานะ':<10}")
    print('='*60)

    for item in assets:
        # item[0]=รหัส, [1]=ชื่อ, [2]=ประเภท, [3]=สถานะ
        print(f'{item[0]:<10} {item[1]:<25} {item[2]:<10} {item[3]:<10}')
    print('='*60)

def add_asset(assets):
    print('\n--- + เพิ่มทรัพย์สินใหม่ ---')
    code = input('รหัสทรัพย์สิน (เช่น IT-001): ').strip().upper()

    for item in assets:
        if item[0] == code:
            print('❌ รหัสนี้เพิ่มแล้วครับ!')
            return
    
    name = input('ชื่ออุปกรณ์: ').strip()
    category = input('ประเภท (Laptop/PC/Printer): ').strip()
    status = 'ปกติ'

    # เพิ่ม List ใน RAM ก่อน
    assets.append([code, name, category, status])
    # บันทึกลงไฟล์ทันที
    save_assets(assets)
    print(f'✅ เพิ่ม {name} เข้าระบบแล้ว')

def update_status(assets):
    ''' Function แก้ไขสถานะ'''
    print('\n--- 🔧 อัพเดทสถานะ ---')
    target_code = input('ป้อนรหัสทรัพสินย์ที่ต้องการแก้: ').strip().upper()

    found = False

    # 1. วนลูปหา assets ที่รหัสตรงกับ target_code
    for item in assets:
        if item[0] == target_code:
            print(f'เจอแล้ว: {item[1]} (สถานะปัจจุบัน: {item[3]})')

            # 2. รับค่าสถานะใหม่
            new_status = input('เปลี่ยนสถานะเป็น (ปกติ/ส่งซ่อม/เสีย): ').strip()

            # 3. อัพเดทค่าใน List item[3]
            item[3] = new_status
            found = True
            print('✅ แก้ไขเรียบร้อย')
            break
    # เช็คว่าหาเจอหรือไม่
    if found:
        # 4. ถ้าหาเจอ ให้บันทึก List ก้อนใหม่ที่แก้ไขแล้ว ทับลงไปในไฟล์เดิม
        save_assets(assets)
    else:
            print('❌ ไม่พบรหัสนี้ในระบบครับ')

def delete_asset(assets):
    print('\n--- ลบรายการทรัพย์สิน ---')
    target_code = input('ป้อนรหัสที่ต้องการลบ: ').strip().upper()

    found = False

    # วนลูปหาตัวที่จะลบ
    for item in assets:
        # item[0] คือรหัสทรัพย์สิน
        if item[0] == target_code:
            print(f'เจอรายการ: {item[1]} (สถานะ: {item[3]})')

            # ถามเพื่อยีนยันการลบ (Safety)
            confirm = input('ยืนยันการลบไหม? (y/n): ').strip().lower()

            if confirm == 'y':
                assets.remove(item) # คำสั่งลบทรัพย์สิน
                found = True
                print('✅ ลบเรียบร้อยแล้ว!')
                break
            else:
                print('ยกเลิกการลบครับ')
                return
    if found:
        save_assets(assets) # บันทึก List ก้อนใหม่ที่สั่งลบข้อมูลไปแล้ว ทับลงไฟล์เดิม
    else:
        print('❌ ไม่พบรหัสนี้ครับ')


def main():
    while True:
        # โหลดข้อมูลใหม่ทุกครั้งที่วนลูป
        my_assets = load_assets()

        print('\n=== 💻 ระบบทะเบียนคุมทรัพย์สิน IT (IT Asset) ===')
        print(f'จำนวนรายการทั้งหมด: {len(my_assets)} รายการ')
        print('[S] แสดงรายการทั้งหมด')
        print('[A] เพิ่มรายการใหม่')
        print('[U] อัพเดทสถานะ (ส่งซ่อม/คืน)')
        print('[D] ลบรายการทรัพย์สิน')
        print('[Q] ออกจากโปรแกรม')

        choice = input('เลือกคำสั่ง: ').upper().strip()

        if choice == 'S':
            show_all_assets(my_assets)
        elif choice == 'A':
            add_asset(my_assets)
        elif choice == 'U':
            update_status(my_assets)
        elif choice == "D":
            delete_asset(my_assets)
        elif choice == 'Q':
            print('ปิดระบบ... บ๊าย บาย 🙏')
            break
        else:
            print('คำสั่งไม่ถูกต้องครับ')

if __name__ == '__main__':
    main()
        