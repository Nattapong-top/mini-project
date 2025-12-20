import contract_manager as manager  # เรืยกใช้ เครื่องมือ

def main():
    while True:
        # โหลดข้อมูลทุกครั้งที่ loop
        my_contracts = manager.load_contracts()

        print('\n=== สมุดโทรศัพท์ป๋า (Contract Book) ===')
        print(f'มีเพื่อนทั้งหมด: {len(my_contracts)} คน')
        print('[S] แสดงรายชื่อทั้งหมด')
        print('[A] เพิ่มรายชื่อใหม่')
        print('[U] แก้ไขรายชื่อ')
        print('[D] ลบรายชื่อ')
        print('[Q] ออกจากโปรแกรม')

        choice = input('เลือกคำสั่ง: ').strip().upper()

        if choice == 'S':
            pass
        elif choice == 'A':
            pass
        elif choice == 'U':
            pass
        elif choice == 'D':
            pass
        elif choice == 'Q':
            print('ออกจากโปรแกรม! บ๊าย บาย')
            break
        else:
            print('เลือกคำสั่งไม่ถูกต้อง!')

if __name__ == '__main__':
    main()


