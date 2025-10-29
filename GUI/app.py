import customtkinter as ctk
import datetime
from tkinter import messagebox

from Invoice import Invoice 

class InvoiceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title('โปรแกรมบันทึกบิลค่าเช่า')
        self.geometry('500x700')
    
        # ตั้งค่า Theme ให้ดูทันสมัย
        ctk.set_appearance_mode('Dark')
        ctk.set_default_color_theme('blue')
        
        # สร้าง Frame หลัก
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=20,
                            fill='both', expand=True)
    
        # ส่วนหัว
        self.title_label = ctk.CTkLabel(self.main_frame,
            text='กรอกข้อมูลบิล', font=ctk.CTkFont(size=20,
            weight='bold'))
        self.title_label.pack(pady=10)
    
        # สร้างข่องกรอกข้อมูล (Entries)งวงวสสาสา
        # ใช้ .grid() เพื่อจัดแถวให้สวยงาม
        self.form_frame = ctk.CTkFrame(self.main_frame,
            fg_color='transparent')
        self.form_frame.pack(pady=10, padx=10)
    
        self.tenant_label = ctk.CTkLabel(self.form_frame, text='ชื่อผู้เช่า:')
        self.tenant_label.grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.tenant_entry = ctk.CTkEntry(
            self.form_frame,placeholder_text='เช่น คุณรักสำราญ สุขรุ่งเรือง', width=250)
        self.tenant_entry.grid(row=0, column=1, padx=10, pady=5)
        self.tenant_entry.insert(0, 'รักสำราญ สุขรุ่งเรือง')
        
        self.room_number_label = ctk.CTkLabel(self.form_frame, text='เลขห้อง:')
        self.room_number_label.grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.room_number_entry = ctk.CTkEntry(
            self.form_frame, placeholder_text='เช่น N01 / 101', width=250)
        self.room_number_entry.grid(row=1, column=1, padx=10, pady=5)
        self.room_number_entry.insert(1, 'N01 / 101')

        # มิเตอร์น้ำ ก่อน - ปัจจุบัน
        self.water_label = ctk.CTkLabel(self.form_frame, text='มิเตอร์น้ำ (ก่อน - ปัจจุบัน):')
        self.water_label.grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.water_prev_entry = ctk.CTkEntry(self.form_frame, width=120)
        self.water_prev_entry.grid(row=2, column=1, sticky='w', padx=10, pady=5)
        self.water_prev_entry.insert(0, '675')

        self.water_curr_entry = ctk.CTkEntry(self.form_frame, width=120)
        self.water_curr_entry.grid(row=2, column=1, sticky='e', padx=10, pady=5)
        self.water_curr_entry.insert(0, '681') 

        # ค่ามิเตอร์ไฟฟ้า ก่อน - ปัจจุบัน
        self.elec_label = ctk.CTkLabel(self.form_frame, text="มิเตอร์ไฟฟ้า (ก่อน - ปัจจุบัน)")
        self.elec_label.grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.elec_prev_entry = ctk.CTkEntry(self.form_frame, width=120)
        self.elec_prev_entry.grid(row=3, column=1, sticky='w', padx=10, pady=5)
        self.elec_prev_entry.insert(0, '591')

        self.elec_curr_entry = ctk.CTkEntry(self.form_frame, width=120)
        self.elec_curr_entry.grid(row=3, column=1, sticky='e', padx=10, pady=5)
        self.elec_curr_entry.insert(0, '636')

        # ปุ่มคำนวณ
        self.calculate_button = ctk.CTkButton(self.main_frame, text='คำนวณยอดบิล',
                                command=self.calculate_invoice) # <-- เชื่อมปุ่มกับฟังก์ชัน
        self.calculate_button.pack(pady=20, ipady=10)

        # ช่องแสดงผลลัพธ์
        self.result_frame = ctk.CTkFrame(self.main_frame, fg_color='#2D2D2D')
        self.result_frame.pack(pady=10, padx=10, fill='x')

        self.result_label_title = ctk.CTkLabel(self.result_frame, text='ยอดรวมสุทธิ:',
                                                font=ctk.CTkFont(size=16))
        self.result_label_title.grid(row=0, column=0, padx=10, pady=10)
        
        self.result_label_value = ctk.CTkLabel(self.result_frame, text='0.00 บาท',
                text_color='#00D8A3', font=ctk.CTkFont(size=24, weight='bold'))
        self.result_label_value.grid(row=0, column=1, padx=10, pady=10, sticky='e')

        # ช่องแสดงรายละเอียด 
        self.details_label = ctk.CTkLabel(self.main_frame, text='--- รายละเอียด ---', justify='left')
        self.details_label.pack(pady=10)

    def calculate_invoice(self):
        ''' ฟังก์ชันการคำนวณยอดบิลค่าเช่าห้อง '''
        print('กำลังคำนวณ...')

        try:
            # ดึงข้อมูลจากช่องกรอก ที่เป็นข้อมูล string
            tenant = self.tenant_entry.get()
            room = self.room_number_entry.get()

            # แปลงค่าจาก str เป็น int 
            # เป็นจะที่อันตราย ถ้ากรอกข้อมูลผิดประเภท เช่น 'abc' อาจจะทำให้โปรแกรมพังได้ 
            w_prev = int(self.water_prev_entry.get())
            w_curr = int(self.water_curr_entry.get())
            e_prev = int(self.elec_prev_entry.get())
            e_curr = int(self.elec_curr_entry.get())

            # ข้อมูลคงที่จากบิล
            rent = 2800.00
            parking_fee = 60.00
            water_rate = 19.00
            elec_rate = 8.00

            # ส่งข้อมูลให้ class Invoice ทำการคำนวณ ข้อมูลที่รับเข้ามา
            invoice_obj = Invoice(
                tenant_name=tenant,
                room_number=room,
                invoice_date=datetime.date.today(), # ใช้วันที่ปัจจุบัน
                room_rent=rent,
                parking_fee=parking_fee,
                water_rate=water_rate,
                electric_rate=elec_rate,
                water_prev_meter=w_prev,
                water_curr_meter=w_curr,
                electric_prev_meter=e_prev,
                electric_curr_meter=e_curr
            )

            # ถ้าข้อมูลไม่ผิด ไม่มี error ก็จะเข้าสู่หน้าแสดงผลลัพธ์
            total = invoice_obj.grand_total

            # อัปเดต Label แสดงผล
            self.result_label_value.configure(text=f'{total:,.2f} บาท')

            # สร้างข้อความสำเร็จรูป
            details_text = f'ค่าห้อง: {invoice_obj.room_rent:,.2f} | ค่าที่จอดรถ: {invoice_obj.parking_fee:,.2f}\n'
            details_text += f'ค่าน้ำ: {invoice_obj.water_units} หน่วย = {invoice_obj.water_cost:,.2f} บาท\n'
            details_text += f'ค่าไฟฟ้า: {invoice_obj.electric_units} หน่วย = {invoice_obj.electric_cost:,.2f} บาท\n'

            self.details_label.configure(text=details_text)

        except ValueError as e:
            # ตรวจจับข้อผิดพลาด ป้องกันโปรแกรม error และจบการทำงาน
            print(f'เกิดข้อผิดพลาด: {e}')

            # แสดงหน้าต่าง แจ้งเตือนผู้ใช้ 
            messagebox.showerror('ข้อมูลผิดพลาด', f'กรุณาตรวจสอบข้อมูล: \n{e}')

            # ล้างผลลัพธ์เก่าออก
            self.result_label_value.configure(text='Error')
            self.details_label.configure(text='---- รายละเอียด ----')

        except Exception as e:
            # ดักจับ Error ทั่วไปที่ไม่ได้คาดคิด
            messagebox.showerror('ผิดพลาดไม่ทราบสาเหตุ', str(e))

        
if __name__ == '__main__':
    
    # สร้างหน้าต่างโปรแกรม
    app = InvoiceApp()      # สร้างหน้าต่างโปรแกรม
    app.mainloop()          # รันโปรแกรม
      
    
    