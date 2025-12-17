import os
# หาทีอยู่ของไฟล์ main.py ปัจจุบัน
script_dir = os.path.dirname(__file__)
# สร้าง path ของ ไฟล์ xxx.txt โดยอ้างอิงจากที่อยู่ของ main.py
file_path = os.path.join(script_dir) + '\\'

def calculate_grade(score):
    '''
    รับคะแนน (int) คืนค่าเป็นเกรด (str)
    '''
    if score >= 80:
        return 'A'
    elif score >= 70:
        return 'B'
    elif score >= 60:
        return 'C'
    elif score >= 50:
        return 'D'
    else:
        return 'F'

def save_grade(filename, name, score, grade):
    '''
    บันทึกข้อมูลต่อท้ายไฟล์ (Append)
    '''
    with open(filename, 'a', encoding='utf-8') as f:
        for i in f:
            f.write(i, name, score, grade, '\n')
        
