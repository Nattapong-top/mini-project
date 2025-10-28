print('โปรแกรมคำนวณค่าไฟฟ้า')

'''
electric_supply_start     = หน่วยเริ่มต้นค่าไฟฟ้า
electric_supply_stop      = หน่วยสุดท้ายค่าไฟฟ้า
electric_rate = 8          = ราคาไฟฟ้าต่อหน่วย
calculate_electric()      = ฟังชันก์การคำนวณค่าไฟฟ้า
calculate_cost         = ตัวแปรเก็บค่าไฟฟ้าจากการคำนวณ
'''

electric_rate = 8

def calculate_electric(start,stop):
    if stop < start:
        print('❌ ข้อมูลไม่ถูกต้อง: หน่วยสุดท้ายต้องมากว่าหรือเท่ากับหน่วยเริ่มต้น')
        return None
    return (stop - start) * electric_rate

# รับค่าจากผู้ใช้
electric_supply_start = int(input('หน่วยเริ่มต้น: '))
electric_supply_stop = int(input('หน่วยสุดท้าย: '))


electric_cost = calculate_electric(electric_supply_start, electric_supply_stop)

if electric_cost is not None:
    print(f'หน่วยค่าไฟฟ้า เริ่มต้นที่ {electric_supply_start} สุดท้ายที่ {electric_supply_stop}')
    print(f'ค่าไฟที่ต้องชำระคือ {electric_cost} บาท')