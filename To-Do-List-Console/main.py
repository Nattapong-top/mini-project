import os
import datetime


# หาที่อยู่ขอไฟล์ main.py ปัจจุบัน
script_dir = os.path.dirname(__file__)
# สร้าง path ของ .txt โดยอิงจากที่อยูของ main.py
file_path = os.path.join(script_dir)


def load_tasks(filename):
    tasks = []

    if not os.path.exists(filename):
        with open(filename, encoding='utf-8') as f:
            for line in f:
                # ตัดช่องว่าง ซ้าย ขวา แล้วเก็บใส่ list เลย ไม่ต้อง split
                task_name = line.strip()
                if task_name: # เช็คว่าไม่ใช่บรรทัดว่าง
                    tasks.append(task_name)
    return tasks

def show_tasks(tasks):
    print("\n" + "="*20)
    print(" 📝 รายการสิ่งที่ต้องทำ")
    print("="*20)

    if not tasks: # ถ้า list ว่าง
        print(" (ว่างเปล่า... สบายจัง!)")
    else:
        for i, t in enumerate(tasks):
            print(f'{i+1}. {t}')
    print("="*20 + '\n')

'''---> ทดลองรันไฟล์ <---'''
my_tasks = load_tasks('todo.txt')
show_tasks(my_tasks)