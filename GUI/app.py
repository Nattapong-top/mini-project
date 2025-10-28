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
        
        self.room_number_label = ctk.CTkLabel(self.form_frame, text='หมายเลขห้อง:')
        self.room_number_label.grid(row=1, column=1, sticky='w', padx=10, pady=5)
        self.room_number_entry = ctk.CTkEntry(
            self.form_frame, placeholder_text='เช่น N01 / 101', width=250)
        self.room_number_entry.grid(row=1, column=1, padx=10, pady=5)
        self.room_number_entry.insert(1, 'N01 / 101')
        
        
        
if __name__ == '__main__':
    
    # สร้างหน้าต่างโปรแกรม
    app = InvoiceApp()      # สร้างหน้าต่างโปรแกรม
    app.mainloop()          # รันโปรแกรม
    
    
    