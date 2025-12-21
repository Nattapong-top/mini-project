import booking_lib as lib

def main():
    while True:
        my_bookings = lib.load_booking()
        print('\n=== 📅 ระบบจองห้องประชุม (Room Booking) ===')
        print('[S] ดูตารางห้องทั้งหมด')
        print('[B] จองห้อง (Book)')
        print('[Q] ออกจากโปรแกรม')

        choice = input('เลือกคำสั่ง: ').strip().upper()

        if choice == 'S':
            lib.show_schedule(my_bookings)
        elif choice == 'B':
            lib.book_room(my_bookings)
        elif choice == 'Q':
            print('ออกจากโปรแกรม... บ๊าย บาย')
            break
        else:
            print('คำสั่งไม่ถูกต้อง')

if __name__ == '__main__':
    main()