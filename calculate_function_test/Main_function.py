room_rate = int(2800)
tv_rate = int(60)
water_rate = int(19)
electric_rate = int(8)


def calculate_room(rent=room_rate,tv=tv_rate):
    return rent + tv

def calculate_electric(start = 0, stop = 0):
    # if stop < start:
    #     print('❌ ข้อมูลไม่ถูกต้อง: หน่วยสุดท้ายต้องมากว่าหรือเท่ากับหน่วยเริ่มต้น')
    #     return None
    return (stop - start) * electric_rate

def calculate_water(start = 0, stop = 0):
    # if stop < start:
    #     print('❌ ข้อมูลไม่ถูกต้อง: หน่วยสุดท้ายต้องมากว่าหรือเท่ากับหน่วยเริ่มต้น')
    #     return None
    return (stop - start) * water_rate


def main():
    print('โปรแกรมคำนวณค่าเช่าห้องอพาร์ทเม้นท์')
    
    # คำนวณค่าห้อง
    print('คำนวณค่าห้องเช่า')
    room_rent_input = input(f'ค่าเช่าห้อง {room_rate} บาท (กด enter เพื่อใช้ค่าเดิม): ')
    room_rent = int(room_rent_input) if room_rent_input.strip() else room_rate
    # เทคนิกการรับ input แบบมีค่าเริ่มต้น ถ้าไม่เปลี่ยนค่าจะใช้ค่าเริ่มต้น ถ้าเปลี่ยนจะใช้ค่าที่เปลี่ยน

    tv_service_input = input(f'ค่าเคบิลทีวี {tv_rate} บาท (กด enter เพื่อใช้ค่าเดิม): ')
    tv_service = int(tv_service_input) if tv_service_input.strip() else tv_rate
    # เทคนิกการรับ input แบบมีค่าเริ่มต้น ถ้าไม่เปลี่ยนค่าจะใช้ค่าเริ่มต้น ถ้าเปลี่ยนจะใช้ค่าที่เปลี่ยน

    room_cost = calculate_room(room_rent, tv_service)
    
    
    # คำนวณค่าไฟฟ้า
    print('คำนวณค่าไฟฟ้า')
    electric_supply_start = int(input('หน่วยเริ่มต้น: '))
    electric_supply_stop = int(input('หน่วยสุดท้าย: '))

    electric_cost = calculate_electric(electric_supply_start, electric_supply_stop)
    
    # คำนวณค่าน้ำ
    print('คำนวณค่าน้ำ')
    water_supply_start = int(input('หน่วยเริ่มต้น: '))
    water_supply_stop = int(input('หน่วยสุดท้าย: '))
    
    water_cost = calculate_water(water_supply_start,water_supply_stop)
    
    # ===== รวม =====
    total_cost = room_cost + electric_cost + water_cost
    print("\n=== ใบแจ้งค่าใช้จ่าย ===")
    print(f"ค่าห้อง       : {room_cost} บาท")
    print(f"ค่าน้ำ        : {water_cost} บาท")
    print(f"ค่าไฟ         : {electric_cost} บาท")
    print(f"รวมทั้งหมด    : {total_cost} บาท")

if __name__ == "__main__":
    main()


