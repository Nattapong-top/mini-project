import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from domain.value_objects import LicensePlate, MoneyThb

class CheckOutFrame(ctk.CTkFrame):
    def __init__(self, master, service, **kwargs):
        super().__init__(master, **kwargs)
        self.service = service

        # --- ส่วนประกอบหน้าจอ ---
        ctk.CTkLabel(self, text="ระบบคิดเงินขาออก", font=("TH Sarabun New", 22, "bold")).pack(pady=10)

        # 1. ช่องกรอกทะเบียน
        self.plate_entry = ctk.CTkEntry(self, placeholder_text="ทะเบียนรถที่ออก", width=200)
        self.plate_entry.pack(pady=5)

        # 2. ปุ่มคำนวณเงิน
        self.btn_calc = ctk.CTkButton(self, text="คำนวณค่าจอด", fg_color="blue", command=self.calculate_fee)
        self.btn_calc.pack(pady=5)

        # 3. พื้นที่แสดงยอดเงิน
        self.fee_label = ctk.CTkLabel(self, text="ยอดที่ต้องชำระ: 0.00 บาท", font=("Arial", 18, "bold"), text_color="yellow")
        self.fee_label.pack(pady=15)

        # 4. ช่องกรอกเงินที่รับมา
        self.payment_entry = ctk.CTkEntry(self, placeholder_text="จำนวนเงินที่รับมา (บาท)", width=200)
        self.payment_entry.pack(pady=5)

        # 5. ปุ่มยืนยัน
        self.btn_pay = ctk.CTkButton(self, text="ยืนยันการจ่ายเงิน & เปิดไม้กั้น", fg_color="green", command=self.confirm_payment)
        self.btn_pay.pack(pady=20)

    def calculate_fee(self):
        try:
            plate = LicensePlate(value=self.plate_entry.get().strip())
            # ดึงตั๋วมาดูเพื่อคำนวณเงินเฉยๆ (ยังไม่เซฟ)
            ticket = self.service.repository.get_by_plate(plate)
            if not ticket:
                messagebox.showerror("Error", "ไม่พบรถคันนี้ครับป๋า")
                return

            fee = ticket.calculate_fee(datetime.now(), self.service.policy)
            self.fee_label.configure(text=f"ยอดที่ต้องชำระ: {fee.value} บาท")
            self.payment_entry.insert(0, str(fee.value)) # ใส่ยอดให้อัตโนมัติเลยป๋าจะได้ไม่ต้องพิมพ์
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def confirm_payment(self):
        try:
            plate = LicensePlate(value=self.plate_entry.get().strip())
            payment_val = float(self.payment_entry.get())
            
            # เรียกใช้ Service ตัวที่ป๋าทำผ่าน 10/10 เมื่อกี้เลย!
            ticket, fee = self.service.process_payment(
                plate=plate,
                payment=MoneyThb(value=payment_val),
                current_time=datetime.now()
            )
            
            messagebox.showinfo("สำเร็จ", f"ชำระเงินเรียบร้อย {fee.value} บาท\nไม้กั้นเปิดแล้วครับป๋า!")
            self.reset_form()
            
        except Exception as e:
            messagebox.showerror("จ่ายเงินพลาด", f"ป๋าครับ! : {str(e)}")

    def reset_form(self):
        self.plate_entry.delete(0, 'end')
        self.payment_entry.delete(0, 'end')
        self.fee_label.configure(text="ยอดที่ต้องชำระ: 0.00 บาท")