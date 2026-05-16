import os

'''โปรเจคที่ 2: โปรแกรมตัดเกรดนักเรียน (Grade Calculator)
เป้าหมาย: ฝึก Logic การคิดคำนวณและการจัดรูปแบบข้อมูล
ฟังก์ชัน: รับชื่อและคะแนนสอบ -> คำนวณเกรด (A, B, C...) -> บันทึกผลลงไฟล์ grades.txt -> สรุปว่ามีคนได้ A กี่คน
สกิลที่ได้: if-elif-else ที่ซับซ้อนขึ้น, การคำนวณทางคณิตศาสตร์, การนับจำนวนใน List'''

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
        f.write(f'{name}, {score}, {grade}\n')
    print('บันทึกข้อมูลลงในไฟล์เรียบร้อย!')

def show_studens(file_studens):
    '''แสดงรายชื่อนักเรียนที่เพิ่มเข้าระบบทั้งหมด'''
    print('แสดงรายชื่อนักเรียนที่เพิ่มเข้าระบบทั้งหมด')

    if os.path.exists(file_studens):
        with open(file_studens, encoding='utf-8') as lines:
            studens = lines.readlines() # อ่านทุกบรรทัดมาเก็บใน list ชื่อ studens

            for i, s in enumerate(studens):
                print(f'{i+1}. {s.strip('\n')}')
            
            # นับจำนวนของ list แทน การใช้ตัวแปร i+1 แบบนี้โปรแกรมจะไม่ error
            print(f'คำนวณเกรดนักเรียนจำนวน {len(studens)} คน')
    else:
        print(f'ยังไม่มีข้อมูลนักเรียนครับ')

def main():
    filename = file_path + 'grades.txt'
    print('=== โปรแกรมตัดเกรดนักเรียน ===')

    while True:
        name = input('\nชื่อนักเรียน (หรือพิมพ์ \'q\' เพื่อจบ): ')

        if name == 'q':
            break

        score_str = input('คะแนนสอบ (0-100): ')
        # ป้องกัน error: ถ้า user พิมพ์ไม่ใช่ตัวเลข
        if not score_str.isdigit():
            print('❌ กรุณาใส่คะแนนเป็นตัวเลขครับ')
            continue
    
        score = int(score_str)

        grade = calculate_grade(score)

        print(f'--> คุณ {name} ได้เกรด: [{grade}]')
        save_grade(filename, name, score, grade)
    
    # แสดงชื่อนักเรียนทั้งหมด
    show_studens(filename)

    print('จบการทำงาน คำนวณเกรดเรียบร้อยครับ!')

if __name__ == '__main__':
    main()
