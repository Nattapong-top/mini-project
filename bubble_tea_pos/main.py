import os

# หาที่อยู่ขอไฟล์ main.py ปัจจุบัน
script_dir = os.path.dirname(__file__)
# สร้าง path ของ menu.txt โดยอิงจากที่อยูของ main.py
file_path = os.path.join(script_dir, 'menu.txt')
file_sales = os.path.join(script_dir, 'sales.txt')


def loal_menu(filename:str):
    '''
    อ่านไฟล์ menu.txt แล้วคืนค่า list of lists
    ตัวอย่าง return: [['ชานม', 40], ['ชาเขียว', 45]]
    '''
    data = []
    with open(filename, encoding='utf-8') as list_data:
        for line in list_data:
            product, price = line.strip().split(',')
            data.append([product, int(price)])
        return data

menu_list = loal_menu(file_path)
print(menu_list)
        
    
def show_menu(menu_list):
    ''' 
    รับ List เมนูร้านชานม ป๋า POS ^_^ _/|\_
    '''
    print('='*30)
    print('     เมนูร้านชานม ป๋า POS ^_^ _/|\_     ')
    print('='*30)
    for i, p in enumerate(menu_list):
        print( f'{i+1}. {p[0]}{p[1]:>10}')

show_menu(menu_list)


def save_sale(items, total):
    '''
    บันทึกรายการขายลงไฟล์ sales.txt
    '''
    # เปิดไฟล์ sales.txt ในโหมด 'a' (append) เพื่อต่อท้ายข้อมูลเดิม
    # เขียนวันที่ (ถ้าทำได้) หรือเขียนแค่รายการและราคารวม
    with open(file_sales) as sale_list:
        sale_list.write(items, total)




