import customtkinter as ctk
from datetime import datetime
import sys
import os

# เพิ่ม Path เพื่อให้ Python มองเห็น Folder src
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import ของที่ป๋าทำมาทั้งหมด
from domain.services import ParkingRegistrationService
from domain.models import PricingPolicy, LicensePlate
from adapters.sqlite_repository import SqliteParkingRepository
from src.ui.app import ParkingApp # หน้า Check-in ที่เราคุยกัน
# สมมติป๋าแยกหน้า Checkout ไว้ หรือจะเขียนรวมในนี้เลยก็ได้

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Paa Top IT Parking System - DDD & Clean Architecture")
        self.geometry("500x600")
        ctk.set_appearance_mode("dark")

        # 1. Setup Backend (อาวุธหลังบ้าน)
        self.repo = SqliteParkingRepository()
        self.repo.create_tables()
        self.policy = PricingPolicy()
        
        # ป๋าใช้ Spy ไปก่อนเพื่อ Demo นะครับ (ไม่ต้องต่อไม้กั้นจริง)
        class BarrierSpy:
            def open(self): print("--- ไม้กั้นเปิดแล้วจ้าป๋า! ---")
        
        self.service = ParkingRegistrationService(
            barrier=BarrierSpy(), 
            repository=self.repo, 
            policy=self.policy
        )

        # 2. สร้าง Tabs (เพื่อปิดจ๊อบให้สวยงาม)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.tab_in = self.tabview.add("รถเข้า (Check-in)")
        self.tab_out = self.tabview.add("รถออก (Check-out)")

        self.setup_checkin_tab()
        self.setup_checkout_tab()

    def setup_checkin_tab(self):
        # ดึง Logic จากที่ป๋าทำใน app.py มาวาง
        ctk.CTkLabel(self.tab_in, text="ทะเบียนรถขาเข้า", font=("Arial", 20)).pack(pady=10)
        self.entry_in = ctk.CTkEntry(self.tab_in, placeholder_text="รวย-999")
        self.entry_in.pack(pady=10)
        ctk.CTkButton(self.tab_in, text="บันทึกรถเข้า", command=self.do_in).pack(pady=10)

    def setup_checkout_tab(self):
        ctk.CTkLabel(self.tab_out, text="ทะเบียนรถขาออก", font=("Arial", 20)).pack(pady=10)
        self.entry_out = ctk.CTkEntry(self.tab_out, placeholder_text="รวย-999")
        self.entry_out.pack(pady=10)
        self.lbl_fee = ctk.CTkLabel(self.tab_out, text="ยอดเงิน: 0 บาท", font=("Arial", 18, "bold"))
        self.lbl_fee.pack(pady=10)
        ctk.CTkButton(self.tab_out, text="คำนวณและจ่ายเงิน", fg_color="green", command=self.do_out).pack(pady=10)

    def do_in(self):
        from domain.value_objects import LicensePlate
        # 1. ดึงค่าและตัดช่องว่างหัวท้ายออก
        plate_str = self.entry_in.get().strip()
        
        # 2. เช็คก่อนส่ง: ถ้าว่าง ป๋าไม่ต้องส่งไปให้ Pydantic ด่าครับ
        if not plate_str:
            from tkinter import messagebox
            messagebox.showwarning("เตือนสติ", "ป๋าครับ! ใส่ทะเบียนรถก่อนสิ")
            return
        
        try:
            plate = LicensePlate(value=self.entry_in.get())
            self.service.register_entry(plate, datetime.now())
            ctk.CTkLabel(self.tab_in, text=f"สำเร็จ: {plate.value} เข้าแล้ว", text_color="green").pack()
        except Exception as e:
            print(f"Error: {e}")

    def do_out(self):
            from domain.value_objects import LicensePlate, MoneyThb
            from tkinter import messagebox
            
            # 1. ดึงค่าและเช็คค่าว่าง (ป้องกัน Pydantic Error)
            plate_str = self.entry_out.get().strip()
            if not plate_str:
                messagebox.showwarning("เตือนสติ", "ป๋าครับ! ต้องใส่ทะเบียนรถขาออกด้วยนะ")
                return

            try:
                plate = LicensePlate(value=plate_str)
                
                # 2. ไปดึงตั๋วมาจากโกดัง
                ticket = self.repo.get_by_plate(plate)
                
                # 3. เช็คก่อนว่าเจอรถไหม (ป้องกัน NoneType Error)
                if ticket is None:
                    self.lbl_fee.configure(text="ยอดเงิน: ไม่พบรถคันนี้จอดอยู่", text_color="red")
                    messagebox.showerror("ไม่พบข้อมูล", f"ป๋าครับ! รถทะเบียน {plate_str} ไม่ได้อยู่ในระบบนะ")
                    return

                # 4. ถ้าเจอรถ ก็คำนวณเงินและโชว์ยอด
                fee = ticket.calculate_fee(datetime.now(), self.policy)
                self.lbl_fee.configure(text=f"ยอดเงินที่ต้องจ่าย: {fee.value} บาท", text_color="yellow")
                
                # 5. เรียก Service ประมวลผลการจ่ายเงิน
                # (ใน Demo นี้สมมติว่าลูกค้าจ่ายครบเท่ากับค่า fee เลยครับ)
                self.service.process_payment(plate, fee, datetime.now())
                
                messagebox.showinfo("สำเร็จ", f"รถ {plate_str} จ่ายเงิน {fee.value} บาท\nไม้กั้นเปิดแล้วครับป๋า!")
                self.entry_out.delete(0, 'end')
                self.lbl_fee.configure(text="ยอดเงิน: 0 บาท", text_color="white")

            except Exception as e:
                messagebox.showerror("เกิดข้อผิดพลาด", f"ป๋าครับ! ระบบขัดข้อง: {str(e)}")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()