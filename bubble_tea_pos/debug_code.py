import os
import datetime

def load_menu(filename:str):
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

# menu_list = load_menu('menu.txt')
# print(menu_list)
        
    
def show_menu(menu_list):
    ''' 
    รับ List เมนูร้านชานม ป๋า POS ^_^ _/|\_
    '''
    print('='*30)
    print('   เมนูร้านชานม ป๋า POS ^_^ _/|\_     ')
    print('='*30)
    for i, p in enumerate(menu_list):
        print(f'{i+1}. {p[0]:15}{p[1]:>10}')
        # print(str(i+1).ljust(2),str(p[0]).ljust(10),str(p[1]).rjust(5))

# show_menu(menu_list)


def save_sale(items, total):
    '''
    บันทึกรายการขายลงไฟล์ sales.txt
    '''
    # เปิดไฟล์ seles.txt ในโหลด 'a' (append) เพื่อต่อท้ายข้อมูลเดิม
    # เขียนวันที่ (ถ้าทำได้) หรือเขียนแต่รายการและราคารวม
    filename = 'sales.txt'
    with open(filename, 'a', encoding='utf-8') as data:
        data.write(datetime.time.datetime, items, total)


def main():
    # --- ส่วนเริ่มต้น ---
    filename = 'menu.txt'
    
    # ตรวจสอบว่ามีไฟล์เมนูไหม
    if not os.path.exists(filename):
        print("หาไฟล์เมนูไม่เจอครับป๋า!")
        return

    my_menu = load_menu(filename)
    
    orders = [] # เก็บชื่อเมนูที่ลูกค้าสั่ง
    total_price = 0
    
    while True:
        # --- ส่วนแสดงผลและรับคำสั่ง ---
        show_menu(my_menu)
        print(f"\nรายการปัจจุบัน: {orders}")
        print(f"ราคารวม: {total_price} บาท\n")
        
        choice = input("เลือกเมนู (ใส่เลข) หรือพิมพ์ 'q' เพื่อจบ/คิดเงิน: ")
        
        if choice == 'q':
            break
            
        # --- ส่วนประมวลผล (Logic) ---
        # 1. ตรวจสอบว่า choice เป็นตัวเลขไหม
        # 2. แปลงเป็น index ของ list (ระวังเรื่อง index เริ่มที่ 0 แต่เมนูเราอาจจะโชว์เลข 1)
        # 3. ดึงชื่อและราคาจาก my_menu มาบวกใส่ orders และ total_price
        
    # --- ส่วนจบการทำงาน ---
    if total_price > 0:
        print(f"\n>>> สรุปยอดเงินทั้งสิ้น: {total_price} บาท <<<")
        save_sale(orders, total_price)
        print("บันทึกยอดขายเรียบร้อย! ขอบคุณที่อุดหนุนครับ")
    else:
        print("ไม่ได้มีการสั่งซื้อ")

# เรียกใช้งานโปรแกรม
if __name__ == "__main__":
    main()





