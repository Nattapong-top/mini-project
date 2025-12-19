print('โปรแกรมคำนวณค่าห้อง')
'''
room_rate           =   ค่าเช่าห้องเริ่มต้น
tv_rate             =   ค่าเคเบิลทีวี
calculate_room      =   ฟังชันก์การคำนวณค่าห้อง
room_rent_input     =   รับค่าห้องเช่าแบบตัวอักษร เพื่อรับเทคนิคการกด enter เพื่อใส่ค่าเดิม
room_rent           =   ค่าห้องเช่าตัวเลข พร้อมนำไปคำนวณ
tv_service_input    =   รับค่าเคเบิลทีวีแบบตัวอักษร เพื่อรับเทคนิคการกด enter 
tv_service          =   ค่าเคเบิลทีวีแบบตัวเลข พร้อมนำไปคำนวณ
room_cost           =   ค่าห้อง + ค่าทีวิ
'''
room_rate = 2800
tv_rate = 60

def calculate_room(rent, tv):
    return rent + tv

# เทคนิกการรับ input แบบมีค่าเริ่มต้น ถ้าไม่เปลี่ยนค่าจะใช้ค่าเริ่มต้น ถ้าเปลี่ยนจะใช้ค่าที่เปลี่ยน
room_rent_input = input(f'ค่าเช่าห้อง {room_rate} บาท (กด enter เพื่อใช้ค่าเดิม): ')
room_rent = int(room_rent_input) if room_rent_input.strip() else room_rate

# เทคนิกการรับ input แบบมีค่าเริ่มต้น ถ้าไม่เปลี่ยนค่าจะใช้ค่าเริ่มต้น ถ้าเปลี่ยนจะใช้ค่าที่เปลี่ยน
tv_service_input = input(f'ค่าเคบิลทีวี {tv_rate} บาท (กด enter เพื่อใช้ค่าเดิม): ')
tv_service = int(tv_service_input) if tv_service_input.strip() else tv_rate



room_cost = calculate_room(room_rent,tv_service)

print(f'ค่าห้อง {room_cost} บาท')