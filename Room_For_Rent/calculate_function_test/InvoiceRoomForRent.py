import datetime


class Invoice:
    """
    คลาสสำหรับสร้างและคำนวณใบแจ้งหนี้ค่าเช่าอพาร์ทเมนท์
    """
    
    def __init__(self,
                 tenant_name: str,
                 room_number: str,
                 invoice_date: datetime.date,
                 room_rent: float,
                 parking_fee: float,
                 water_rate: float,
                 electric_rate: float,
                 water_prev_meter: int,
                 water_curr_meter: int,
                 electric_prev_meter: int,
                 electric_curr_meter: int
                 ) -> None:

        # ---- ข้อมูลที่รับเข้ามา (Attribute) ----
        self.tenant_name = tenant_name
        self.room_number = room_number
        self.invoice_date  = invoice_date
        
        # ---- ค่าใช้จ่ายคงที่ ----
        self.room_rent = room_rent
        self.parking_fee = parking_fee
        
        # ---- อัตราค่าบริการ ----
        self.water_rate = water_rate
        self.electric_rate = electric_rate
        
        # ---- ข้อมูลมิตเตอร์ ====
        self.water_prev_meter = water_prev_meter
        self.water_curr_meter = water_curr_meter
        
        self.electric_prev_meter = electric_prev_meter
        self.electric_curr_meter = electric_curr_meter
        
    # ---- Method ส่วนของการคำนวณ ค่าใข้จ่ายต่างๆ  ----
    # ==== ใช้ @property เพือ่ให้การคำนวณดูเหมือนเป็น คุณสมบัติ ----
    
    @property
    def water_curr_meter(self) -> int:
        # --- Gutter สำหรับ _water_curr_meter ---
        return self._water_curr_meter
    
    @water_curr_meter.setter
    def water_curr_meter(self, value: int):
        """
        นี่คือ Setter !
        มันจะทำงาน "อัตโนมัติ" ทุกครั้งที่มีการกำหนดค่าให้
        self.water_curr_meter = (ค่าใหม่)
        """
        print(f'[Setter] ตรสจสอบค่ามิเตอร์น้ำปัจจุบัน: {value}')
        if value < self.water_prev_meter:
            # ถ้าค่าใหม่น้อยกว่าค่าเก่า -> ข้อมูลผิด!
            raise ValueError('เลขมิเตอร์ปัจจุบัน ต้องไม่น้อยกว่าเลขมิเตอร์ก่อนหน้านี้')
        
        # ถ้าข้อมูลถูกต้อง ก็เก็บลงในตัวแปร private 
        self._water_curr_meter = value
    
    @property
    def water_units(self) -> int:
        # --- คำนวณจำนวนหน่วยน้ำที่ใช้ ---
        return self.water_curr_meter - self.water_prev_meter

    @property
    def water_cost(self) -> float:
        # ---- คำนวณค่าใช้จ่ายน้ำ ----
        return self.water_units * self.water_rate
    
    @property
    def electric_curr_meter(self) -> int:
        # --- Getter สำหรับ _electric_curr_meter ---
        return self._electric_curr_meter
    
    @electric_curr_meter.setter
    def electric_curr_meter(self, value: int):
        """
        นี่คือ Setter !
        มันจะทำงาน "อัตโนมัติ" ทุกครั้งที่มีการกำหนดค่าให้
        self.water_curr_meter = (ค่าใหม่)
        """
        print(f'[Setter] ตรวจสอบมิเตอร์ไฟฟ้าปัจจุบัน: {value}')
        if value < self.electric_prev_meter:
            # ถ้าค่าใหม่น้อยกว่าค่าเก่า -> ข้อมูลผิด
            raise ValueError('เลขมิเตอร์ปัจจุบันต้อง ไม่น้อยกว่าเลขมิเตอร์ก่อนหน้า')
        
        # ถ้าข้อมูลถูกต้อง ก็เก็บลงใจตัวแปร private
        self._electric_curr_meter = value
    
    @property
    def electric_units(self) -> int:
        # ---- คำนวณจำนวนหน่วยไฟฟ้าที่ใช้ ----
        return self.electric_curr_meter - self.electric_prev_meter
    
    @property
    def electric_cost(self) -> float:
        # ---- คำนวณค่าใช้จ่ายไฟฟ้า ----
        return self.electric_units * self.electric_rate
    
    @property
    def total_utilities_cost(self) -> float:
        # ---- คำนวณค่าสาธารณูปโภค (น้ำ + ไฟฟ้า + ที่จอดรถ) ----
        return self.water_cost + self.electric_cost + self.parking_fee
    
    @property
    def grand_total(self) -> float:
        # ==== คำนวณยอดรวมสุทธิ ----
        return self.room_rent + self.total_utilities_cost
    
    # ---- Method ส่วนของการแสดงผล ----
    def display_summary(self):
        # ---- แสดงผลสุรปใบแจ้งหนี้ ----
        print('-' * 70)
        print(f'ใบแจ้งหนี้สำหรับ: {self.tenant_name}')
        print(f'ห้อง: {self.room_number} | วันที่: {self.invoice_date.strftime('%d/%m/%Y')}')
        
        print('-' * 70)
        print(f'1. ค่าเช่าห้อง: {self.room_rent:,.2f} บาท')
        
        print(f'2. คำนวณหน่วยน้ำ มิตเตอร์เริ่มต้น: {self.water_prev_meter} - {self.water_curr_meter} = {self.water_units} หน่วย')
        print(f'    คำนวณค่าน้ำ: {self.water_units} * {self.water_rate} = {self.water_cost:,.2f} บาท')
        
        print(f'3. คำนวณหน่วยไฟฟ้า มิตเตอร์เริ่มต้น: {self.electric_prev_meter} - {self.electric_curr_meter} = {self.electric_units} หน่วย')
        print(f'    คำนวณค่าไฟฟ้า: {self.electric_units} * {self.electric_rate} = {self.electric_cost:,.2f} บาท')
        
        print(f'4. ค่าที่จอดรถ: {self.parking_fee:,.2f} บาท')
        print('-' * 70)
        
        print(f'ยอดรวมทั้งสิน: {self.grand_total:,.2f} บาท')
        print('-' * 70)
        

if __name__ == '__main__':
    
    """
    Creating an Instance การสร้าง Object มาใช้งาน
    """
    
    print('========== เริ่มการทำงานของโปรแกรม ==========')
    invoice_n101 = Invoice(
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
    
    # ---- สั่งให้ object ที่เราสร้างขึ้นมา แสดงผล
    invoice_n101.display_summary()