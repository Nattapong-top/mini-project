import unittest
import datetime
from invoice import Invoice 

class TestInvoice(unittest.TestCase):
    def setUp(self):
        print('\n[setUp] กำลังสร้าง invoice ต้นแบบสำหรับเทสต์...')
        self.test_invoice = Invoice(
            tenant_name='รักสำราญ สุขสำเรือง',
            room_number='N101 / 101',
            invoice_date=datetime.date(2025,10,25),
            
            # ---- ค่าใช้จ่ายคงที่ ----
            room_rent=2800.00,
            parking_fee=60.00,
            water_rate=19.00,
            electric_rate=8.00,
            
            # ---- ข้อมูลจากมิตเตอร์ ----
            water_prev_meter=675,
            water_curr_meter=681,
            electric_prev_meter=591,
            electric_curr_meter=636
        )

    
    def test_water_units_calculation(self):
        """
        เทสต์การคำนวณหน่วยน้ำที่ใช้
        คาดหวัง: 681 - 675 = 6 หน่วย
        """
        print("เทสต์ข้อที่ 1: การคำนวณหน่วยน้ำ")
        # self.assertEqual(A, B) คือ "ฉันยืนยันว่า A ต้องเท่ากับ B"
        self.assertEqual(self.test_invoice.water_units, 6)
    
    def test_electric_units_calculation(self):
            """
            เทสต์การคำนวณหน่วยไฟที่ใช้
            คาดหวัง: 636 - 591 = 45 หน่วย
            """
            print("เทสต์ข้อที่ 2: การคำนวณหน่วยไฟ")
            self.assertEqual(self.test_invoice.electric_units, 45)
    
    def test_water_cost_calculation(self):
            """
            เทสต์การคำนวณค่าน้ำ
            คาดหวัง: 6 หน่วย * 19.00 บาท = 114.00 บาท
            """
            print("เทสต์ข้อที่ 3: การคำนวณค่าน้ำ")
            # ใช้ assertAlmostEqual สำหรับเลขทศนิยม (float) จะปลอดภัยกว่า
            self.assertAlmostEqual(self.test_invoice.water_cost, 114.00)
        
    def test_electric_cost_calculation(self):
            """
            เทสต์การคำนวณค่าไฟ
            คาดหวัง: 45 หน่วย * 8.00 บาท = 360.00 บาท
            """
            print("เทสต์ข้อที่ 4: การคำนวณค่าไฟ")
            self.assertAlmostEqual(self.test_invoice.electric_cost, 360.00)

    def test_grand_total_calculation(self):
        """
        เทสต์การคำนวณยอดรวมสุทธิ
        คาดหวัง: 2800 (เช่า) + 60 (เน็ต) + 114 (น้ำ) + 360 (ไฟ) = 3334.00 บาท
        """
        print("เทสต์ข้อที่ 5: การคำนวณยอดรวมสุทธิ")
        self.assertAlmostEqual(self.test_invoice.grand_total, 3334.00)

    def test_total_utilities_cost_calculation(self):
        print("เทสต์ข้อที่ 4.1: คำนวณสาธารณุปโภค")
        self.assertAlmostEqual(self.test_invoice.total_utilities_cost, 534.00)

    def test_edge_case_zero_usage(self):
        """
        เทสต์ "กรณีพิเศษ" (Edge Case) เช่น ถ้าไม่มีการใช้น้ำไฟเลย
        """
        print("เทสต์ข้อที่ 6: กรณีพิเศษ (ไม่มีการใช้งาน)")
        zero_use_invoice = Invoice(
            tenant_name="Test User 2", room_number="T002",
            invoice_date=datetime.date(2025, 10, 25),
            room_rent=2800.00, parking_fee=60.00,
            water_rate=19.00, electric_rate=8.00,
            water_prev_meter=700, water_curr_meter=700,  # <--- ไม่ได้ใช้
            electric_prev_meter=600, electric_curr_meter=600 # <--- ไม่ได้ใช้
        )

        self.assertEqual(zero_use_invoice.water_units, 0)
        self.assertEqual(zero_use_invoice.electric_units, 0)
        self.assertAlmostEqual(zero_use_invoice.grand_total, 2860.00) # (ค่าห้อง + ที่จอดรถ)


    def test_setter_raises_error_on_invalid_water_meter(self):
        '''
        เทสข้อที่ 7 (sad path) :
        ทดสอบว่า setter จะโยน 'ValueError'
        เมื่อใส่เลขมิเตอร์ปัจจุบัน น้อยกว่ามิเตอร์ก่อนหน้า
        '''
        print('\n[setUp] สร้างเทสต์สำหรับ sad path น้ำ') 
        print('เทสข้อที่ 7: การดักจับข้อมูลมิเตอร์น้ำที่ผิดพลาด')
        
        # ใช้ with self.assertRaises(ErrorType)
        # เพื่อ "ดักรอ" ว่าโค้ดข้องในนี้ 'ต้อง' โยน ValueError ออกมา
        with self.assertRaises(ValueError):
            # พยายามสร้าง object ด้วยข้อมูลที่ 'ผิด'
            Invoice(
                tenant_name='Test Water Error User',
                room_number='T-ERROR',
                invoice_date=datetime.date(2025,11,27),
                room_rent=2020, 
                parking_fee=0,
                water_rate=10, 
                electric_curr_meter=5,
                water_curr_meter=200,
                water_prev_meter=100,
            )

    def test_setter_raises_error_on_invalid_electric_meter(self):
        '''
        เทสข้อที่ 8 (sad path) :
        ทดสอบว่า setter จะโยน 'ValueError'
        เมื่อใส่เลขมิเตอร์ปัจจุบัน น้อยกว่ามิเตอร์ก่อนหน้า
        '''
        print('\n[setUp] สร้างเทสต์สำหรับ sad path น้ำ') 
        print('เทสข้อที่ 8: การดักจับข้อมูลมิเตอร์ไฟฟ้าที่ผิดพลาด')
        
        # ใช้ with self.assertRaises(ErrorType)
        # เพื่อ "ดักรอ" ว่าโค้ดข้องในนี้ 'ต้อง' โยน ValueError ออกมา

        # 
        # 
        # 
        # 
        
        with self.assertRaises(ValueError):
            # พยายามสร้าง object ด้วยข้อมูลที่ 'ผิด'
            Invoice(
                tenant_name='Test electric Error User', 
                room_number='T-ERROR',
                invoice_date=datetime.date(2025,11,27),
                room_rent=2020, parking_fee=0,
                electric_curr_meter=200,
                electric_prev_meter=100
            )


    
if __name__ == '__main__':
    unittest.main()