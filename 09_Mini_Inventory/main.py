import inventory_manager as manager

def main():
    while True:
        my_products = manager.load_products()

        print('\n== 🏭 ระบบสต๊อกสินค้า (Mini Inventory) ===')
        print(f'รายการสินค้าทั้งหมด {len(my_products)}')
        print('[S] ดูสต๊อกคงเหลือ')
        print('[A] เพิ่มสินค้าใหม่ (New SKU)')
        print('[U] รับเข้าเบิกออก (Update Stock)')
        print('[Q] ออกจากโปรแกรม')

        choice = input('เลือกคำสั่ง: ').strip().upper()

        if choice == 'S':
            manager.show_all_products(my_products)
        elif choice == 'A':
            manager.add_product(my_products)
        elif choice == 'U':
            manager.update_stock(my_products)
        elif choice == 'Q':
            print('ปิดระบบสต๊อก... บ๊าย บาย')
            break
        else:
            print('คำสั่งไม่ถูกต้อง')

if __name__ == '__main__':
    main()