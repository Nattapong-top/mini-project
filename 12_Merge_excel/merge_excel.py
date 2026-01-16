import customtkinter as ctk
from tkinter import filedialog
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue") 

class ExcelMergerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 1. ตั้งค่าหน้าต่างหลัก ---
        self.title("Excel Merger Pro - By Paa Top IT")
        self.geometry("700x500")
        
        # จัด Layout หลัก: แบ่งเป็น 2 แถว
        # row 0 = Header Bar (ด้านบน)
        # row 1 = Main Content (พื้นที่ทำงาน)
        self.grid_rowconfigure(0, weight=0) # สูงเท่าที่จำเป็น
        self.grid_rowconfigure(1, weight=1) # ขยายเต็มพื้นที่ที่เหลือ
        self.grid_columnconfigure(0, weight=1)

        # ข้อมูลภาษา (เหมือนเดิม)
        self.lang_code = "en"
        self.texts = {
            "en": {
                "title": "Excel Merger Tool",
                "add_file": "Add Files",
                "add_folder": "Add Folder",
                "clear": "Clear List",
                "merge": "MERGE FILES",
                "status_ready": "Ready...",
                "lang_label": "Language:"
            },
            "th": {
                "title": "โปรแกรมรวมไฟล์ Excel",
                "add_file": "เพิ่มไฟล์",
                "add_folder": "เพิ่มโฟลเดอร์",
                "clear": "ล้างรายการ",
                "merge": "เริ่มรวมไฟล์",
                "status_ready": "พร้อมทำงาน...",
                "lang_label": "ภาษา:"
            },
            "cn": {
                "title": "Excel 合并工具",
                "add_file": "添加文件",
                "add_folder": "添加文件夹",
                "clear": "清空列表",
                "merge": "立即合并",
                "status_ready": "准备就绪...",
                "lang_label": "语言:"
            }
        }

        self.create_widgets()
        self.update_language_ui()

    def create_widgets(self):
        # --- A. ส่วนหัวด้านบน (Header Frame) ---
        self.header_frame = ctk.CTkFrame(self, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        
        # ชื่อโปรแกรม (อยู่ซ้ายสุดของ Header)
        self.logo_label = ctk.CTkLabel(self.header_frame, text="Excel Merger", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(side="left", padx=20, pady=10)

        # ตัวเลือกภาษา (อยู่ขวาสุดของ Header)
        self.lang_option = ctk.CTkOptionMenu(self.header_frame, 
                                             values=["English", "ไทย", "中文"],
                                             command=self.change_language_event,
                                             width=100)
        self.lang_option.pack(side="right", padx=20, pady=10)
        
        self.lang_label_ui = ctk.CTkLabel(self.header_frame, text="Language:")
        self.lang_label_ui.pack(side="right", padx=5)


        # --- B. พื้นที่ทำงานหลัก (Main Content) ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent") # transparent เพื่อให้สีกลืนกับพื้นหลัง
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        # แบ่งซ้ายขวา (ซ้าย=รายการไฟล์, ขวา=ปุ่มคำสั่ง)
        self.main_frame.grid_columnconfigure(0, weight=1) # ช่องซ้ายขยายได้
        self.main_frame.grid_columnconfigure(1, weight=0) # ช่องขวาขนาดคงที่
        self.main_frame.grid_rowconfigure(0, weight=1)

        # 1. รายการไฟล์ (Textbox)
        self.file_list_display = ctk.CTkTextbox(self.main_frame)
        self.file_list_display.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.file_list_display.insert("0.0", "...\n")
        self.file_list_display.configure(state="disabled")

        # 2. กลุ่มปุ่มคำสั่ง (Button Column)
        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.grid(row=0, column=1, sticky="ns")

        self.btn_add_file = ctk.CTkButton(self.btn_frame, text="Add Files", command=self.dummy_action)
        self.btn_add_file.pack(pady=(0, 10), fill="x")

        self.btn_add_folder = ctk.CTkButton(self.btn_frame, text="Add Folder", command=self.dummy_action)
        self.btn_add_folder.pack(pady=(0, 10), fill="x")

        self.btn_clear = ctk.CTkButton(self.btn_frame, text="Clear", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.dummy_action)
        self.btn_clear.pack(pady=(0, 20), fill="x")

        # ปุ่ม MERGE (เน้นสี)
        self.btn_merge = ctk.CTkButton(self.btn_frame, text="MERGE", height=60, fg_color="#2CC985", hover_color="#229965", font=ctk.CTkFont(size=16, weight="bold"), command=self.dummy_action)
        self.btn_merge.pack(side="bottom", fill="x")

    def change_language_event(self, new_lang):
        if new_lang == "English": self.lang_code = "en"
        elif new_lang == "ไทย": self.lang_code = "th"
        elif new_lang == "中文": self.lang_code = "cn"
        self.update_language_ui()

    def update_language_ui(self):
        t = self.texts[self.lang_code]
        self.logo_label.configure(text=t["title"])
        self.lang_label_ui.configure(text=t["lang_label"])
        self.btn_add_file.configure(text=t["add_file"])
        self.btn_add_folder.configure(text=t["add_folder"])
        self.btn_clear.configure(text=t["clear"])
        self.btn_merge.configure(text=t["merge"])
    
    def dummy_action(self):
        print("Button Clicked")

if __name__ == "__main__":
    app = ExcelMergerApp()
    app.mainloop()