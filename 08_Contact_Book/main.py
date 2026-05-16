import contract_manager as manager  # เรืยกใช้ เครื่องมือ

def main():
    while True:
        # โหลดข้อมูลทุกครั้งที่ loop
        my_contracts = manager.load_contracts()

        print('\n=== สมุดโทรศัพท์ป๋า (Contract Book) ===')
        print(f'มีเพื่อนทั้งหมด: {len(my_contracts)} คน')
        print('[S] แสดงรายชื่อทั้งหมด')
        print('[F] ค้นหารายชื่อ')
        print('[A] เพิ่มรายชื่อใหม่')
        print('[U] แก้ไขรายชื่อ')
        print('[D] ลบรายชื่อ')
        print('[Q] ออกจากโปรแกรม')

        choice = input('เลือกคำสั่ง: ').strip().upper()

        if choice == 'S':
            manager.show_all_contracts(my_contracts)
        elif choice == "F":
            manager.search_contract(my_contracts)
        elif choice == 'A':
            manager.add_contract(my_contracts)
        elif choice == 'U':
            manager.update_contract(my_contracts)
        elif choice == 'D':
            manager.delete_contract(my_contracts)
        elif choice == 'Q':
            print('ออกจากโปรแกรม! บ๊าย บาย')
            break
        else:
            print('เลือกคำสั่งไม่ถูกต้อง!')

if __name__ == '__main__':
    main()


