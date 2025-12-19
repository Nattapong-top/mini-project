import os

'''โปรเจคที่ 3: ระบบ Login อย่างง่าย (Simple Login System)
เป้าหมาย: จำลองการตรวจสอบสิทธิ์ (Auth)
ฟังก์ชัน: มีไฟล์ users.txt เก็บ (username, password) -> โปรแกรมให้ user กรอก -> ตรวจสอบว่าตรงกับในไฟล์ไหม -> ถ้าตรงให้เข้าระบบ ถ้าไม่ตรงให้ลองใหม่
สกิลที่ได้: การค้นหาข้อมูลใน List (Search), break loop, ความปลอดภัยเบื้องต้น'''

# หาทีอยู่ของไฟล์ main.py ปัจจุบัน
script_dir = os.path.dirname(__file__)
# สร้าง path ของ ไฟล์ xxx.txt โดยอ้างอิงจากที่อยู่ของ main.py
file_path = os.path.join(script_dir) + '\\'

def check_login(filename, input_user, input_pass):
    '''คืนค่า True ถ้า login ผ่าน คืนค่า False ถ้าไม่ผ่าน'''

    if os.path.exists(filename):
        with open(filename, encoding='utf-8') as file_login:
            for lines in file_login:
                # ใช้ .strip() ว่างเพื่อตัดช่องว่างและ \n ได้พร้อมกัน
                parts = lines.strip().split(',')
                # เช็คก่อนว่า ว่าในไฟล์มีข้อมูลสองชุดอย่างที่เราต้องการไหม
                if len(parts) == 2:
                    username, password = parts 
                    if input_user == username and input_pass == password:
                        return True
            # วน loop จนครบแล้วไม่ตรงกันก็ให้ return False
            return False

def main():

    # โหลดไฟล์ xxx.txt
    filename = file_path + 'users.txt'

    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write('admin,123\npapa,9999\n')
    
    print('=== ระบบ Login ง่ายๆ ===')

    # เปลี่ยน loop while เป็น loop for 
    for i in range(3):
        user = input('Usesname: ')
        pwd = input('Password: ')

        if check_login(filename, user, pwd):
            print(f' ยินดีตอนรับคุณ {user}!')
            return # จบ function main (ออกจากโปรแกรม)
        else:
            print(' ข้อมูลไม่ถูกต้อง')
            print(f'เหลือโอกาศอีก {2 - i} ครั้ง')
    
    print(' ระบบล็อก! คุณใส่ผิดเกินกำหนด')

if __name__ == '__main__':
    main()