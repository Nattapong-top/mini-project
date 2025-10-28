print('โปรแกรมคำนวณค่าน้ำ')

'''
warter_supply_start     = หน่วยเริ่มต้นค่าน้ำ
warter_supply_stop      = หน่วยสุดท้ายค่าน้ำ
water_rate  = 19        = ราคาน้ำต่อหน่วย
calculate_warter()      = ฟังชันก์การคำนวณค่าน้ำ
warter_cost         = ตัวแปรเก็บค่าน้ำจากการคำนวณ
'''
water_rate = 19

def calculate_warter(start,stop):
    if stop < start :
        print('❌ ข้อมูลไม่ถูกต้อง: หน่วยสุดท้ายต้องมากว่าหรือเท่ากับหน่วยเริ่มต้น')
        return None
    
    return (stop - start) * water_rate

# รับค่าจากผู้ใช้
warter_supply_start = int(input('หน่วยเริ่มต้น: '))
warter_supply_stop = int(input('หน่วยสุดท้าย: '))



warter_cost = calculate_warter(warter_supply_start,warter_supply_stop)

if warter_cost is not None:
    print(f'หน่วยค่าน้ำเริ่มต้นที่ {warter_supply_start} สุดท้ายที่ {warter_supply_stop}')
    print(f'ค่าน้ำที่ต้องชำระคือ {warter_cost} บาท')


