import os

# หาทีอยู่ของไฟล์ main.py ปัจจุบัน
script_dir = os.path.dirname(__file__)
# สร้าง path ของ ไฟล์ xxx.txt โดยอ้างอิงจากที่อยู่ของ main.py
file_path = os.path.join(script_dir) + '\\'

def check_login(filename, input_user, input_pass):
    '''คืนค่า True ถ้า login ผ่าน คืนค่า False ถ้าไม่ผ่าน'''

    if os.path.exists(filename):
        with open(filename, encoding='utf-8') as file_login:
            for lines in file_login:
                username, password = lines.strip('\n').split(',')
                if input_user == username and input_pass == password:
                    return True
            return False

def main():

    # โหลดไฟล์ xxx.txt
    filename = file_path + 'users.txt'

    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write('admin,123\npapa,9999\n')
    
    print('=== ระบบ Login ง่ายๆ ===')

    attempts = 0
    while attempts < 3:
        user = input('Usesname: ')
        pwd = input('Password: ')

        if check_login(filename, user, pwd):
            print(f' ยินดีตอนรับคุณ {user}!')
            return # จบ function main (ออกจากโปรแกรม)
        else:
            print(' ข้อมูลไม่ถูกต้อง')
            attempts += 1
            print(f'เหลือโอกาศอีก {3 - attempts} ครั้ง')
    
    print(' ระบบล็อก! คุณใส่ผิดเกินกำหนด')

if __name__ == '__main__':
    main()

    

