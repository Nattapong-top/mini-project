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
                username, password = lines.split(',')
            if input_user == username and input_pass == password:
                return True
            else:
                return False

# def main():

#     # โหลดไฟล์ xxx.txt
#     filename = file_path + 'users.txt'

#     if not os.path.exists(filna)
