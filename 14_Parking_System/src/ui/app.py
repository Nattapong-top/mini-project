import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
# อย่าลืมแก้ Path ให้ตรงกับที่ป๋าเก็บไฟล์ไว้นะครับ
from domain.services import ParkingRegistrationService
from domain.value_objects import LicensePlate

class ParkingApp(ctk.CTk):
    def __init__(self, service: ParkingRegistrationService):
        super().__init__()
        self.service = service
        
        self.title("Paa Natthapong Parking System v1.0")
        self.geometry("400x300")
        ctk.set_appearance_mode("dark")

        # --- ส่วนประกอบหน้าจอ ---
        self.label = ctk.CTkLabel(self, text="ระบบลงทะเบียนรถเข้า", font=("TH Sarabun New", 24, "bold"))
        self.label.pack(pady=20)

        self.plate_entry = ctk.CTkEntry(self, placeholder_text="กรอกเลขทะเบียนรถ (เช่น รวย-999)", width=250)
        self.plate_entry.pack(pady=10)

        self.btn_checkin = ctk.CTkButton(self, text="ลงทะเบียนรถเข้า [Check-in]", command=self.do_checkin)
        self.btn_checkin.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="สถานะ: พร้อมใช้งาน", text_color="gray")
        self.status_label.pack(pady=10)

    def do_checkin(self):
        plate_str = self.plate_entry.get().strip()
        
        if not plate_str:
            messagebox.showwarning("คำเตือน", "ป๋าครับ! ลืมกรอกทะเบียนรถหรือเปล่า?")
            return

        try:
            # --- ตรงนี้แหละครับที่ GUI คุยกับ Logic ของเรา ---
            plate = LicensePlate(value=plate_str)
            now = datetime.now()
            
            # เรียกใช้ Service ที่ป๋าอุตส่าห์เขียนมาแทบตาย!
            ticket = self.service.register_entry(plate, now)
            
            # แจ้งผล
            self.status_label.configure(text=f"สถานะ: รถ {plate_str} เข้าแล้ว! ไม้กั้นเปิด!", text_color="green")
            messagebox.showinfo("สำเร็จ", f"ออกตั๋วเลขที่: {plate_str}\nเวลา: {now.strftime('%H:%M:%S')}")
            self.plate_entry.delete(0, 'end') # ล้างช่องกรอก
            
        except Exception as e:
            messagebox.showerror("เกิดข้อผิดพลาด", f"ป๋าครับ! เกิดปัญหา: {str(e)}")

# --- วิธีการรัน (Main) ---
if __name__ == "__main__":
    # 1. เตรียมอาวุธ (Dependencies) เหมือนใน Test เลยครับป๋า!
    from adapters.sqlite_repository import SqliteParkingRepository # ใช้ของจริงแล้ว!
    from domain.barrier_spay import BarrierSpy as  RealBarrierAdapter # สมมติว่ามีตัวต่อไม้กั้นจริง
    from domain.models import PricingPolicy

    # ป๋าต้องไปสร้าง DB ก่อนนะถ้ายังไม่มี
    repo = SqliteParkingRepository() 
    repo.create_tables()
    
    # สร้าง Service
    service = ParkingRegistrationService(
        barrier=RealBarrierAdapter(), # หรือใช้ Spy ไปก่อนก็ได้ถ้ายังไม่มี hardware
        repository=repo,
        policy=PricingPolicy()
    )

    # 2. รัน App
    app = ParkingApp(service)
    app.mainloop()