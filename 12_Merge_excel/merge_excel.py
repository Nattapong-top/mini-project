import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog

# ตั้งค่าธีมเบื้องต้น (System = ตามคอมเรา, Dark, Light)
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue") 

class ExcelMergerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 1. ตั้งค่าหน้าต่างหลัก ---
        self.title("Excel Merger Pro - By Paa")
        self.geometry("700x500")
        
        # --- 2. ข้อมูลภาษา (Dictionary) ---
        self.lang_code = "en" # ภาษาเริ่มต้น
        self.texts = {
            "en": {
                "title": "Excel File Merger",
                "add_file": "Add Files",
                "add_folder": "Add Folder",
                "clear": "Clear List",
                "merge": "MERGE FILES NOW",
                "status_ready": "Ready to start...",
                "file_count": "Files selected: "
            },
            "th": {
                "title": "โปรแกรมรวมไฟล์ Excel",
                "add_file": "เพิ่มไฟล์",
                "add_folder": "เพิ่มโฟลเดอร์",
                "clear": "ล้างรายการ",
                "merge": "เริ่มรวมไฟล์ทันที",
                "status_ready": "พร้อมทำงาน...",
                "file_count": "จำนวนไฟล์ที่เลือก: "
            },
            "cn": {
                "title": "Excel 合并工具",
                "add_file": "添加文件",
                "add_folder": "添加文件夹",
                "clear": "清空列表",
                "merge": "立即合并",
                "status_ready": "准备就绪...",
                "file_count": "选定文件数: "
            }
        }

        # --- 3. สร้าง Widget (หน้าตา) ---
        self.create_widgets()
        
        # อัปเดตภาษาครั้งแรก
        self.update_language_ui()

    def create_widgets(self):
        # Grid layout config (จัดหน้ากระดาษ)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # -- Sidebar ด้านซ้าย (เมนู) --
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Logo / Title
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Merger Tool", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # ปุ่มเลือกภาษา
        self.lang_label = ctk.CTkLabel(self.sidebar_frame, text="Language / ภาษา:", anchor="w")
        self.lang_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        
        self.lang_option = ctk.CTkOptionMenu(self.sidebar_frame, 
                                             values=["English", "ไทย", "中文"],
                                             command=self.change_language_event)
        self.lang_option.grid(row=2, column=0, padx=20, pady=(10, 10))

        # -- พื้นที่หลัก (Main Area) --
        
        # ช่องแสดงรายชื่อไฟล์ (ใช้ Textbox แต่ล็อคไม่ให้พิมพ์)
        self.file_list_display = ctk.CTkTextbox(self, width=250)
        self.file_list_display.grid(row=0, column=1, rowspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.file_list_display.insert("0.0", "No files selected...\n(ยังไม่ได้เลือกไฟล์)")
        self.file_list_display.configure(state="disabled") # ล็อคห้ามพิมพ์เอง

        # -- ปุ่มควบคุมด้านขวา --
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.grid(row=0, column=2, rowspan=3, padx=20, pady=20, sticky="ns")

        self.btn_add_file = ctk.CTkButton(self.btn_frame, text="Add Files", command=self.add_files_action)
        self.btn_add_file.pack(pady=10, padx=10, fill="x")

        self.btn_add_folder = ctk.CTkButton(self.btn_frame, text="Add Folder", command=self.add_folder_action)
        self.btn_add_folder.pack(pady=10, padx=10, fill="x")

        self.btn_clear = ctk.CTkButton(self.btn_frame, text="Clear", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.clear_action)
        self.btn_clear.pack(pady=10, padx=10, fill="x")

        # ปุ่ม MERGE ใหญ่ๆ
        self.btn_merge = ctk.CTkButton(self.btn_frame, text="MERGE", height=50, fg_color="#2CC985", hover_color="#229965", command=self.merge_action)
        self.btn_merge.pack(pady=(20, 10), padx=10, fill="x")

        # Status Bar ด้านล่าง
        self.status_label = ctk.CTkLabel(self, text="Ready", anchor="w")
        self.status_label.grid(row=3, column=1, columnspan=2, padx=20, pady=10, sticky="ew")

    # --- 4. ฟังก์ชันทำงาน (Logic) ---
    
    def change_language_event(self, new_lang):
        # แปลงค่าจาก Dropdown เป็นรหัสภาษา
        if new_lang == "English": self.lang_code = "en"
        elif new_lang == "ไทย": self.lang_code = "th"
        elif new_lang == "中文": self.lang_code = "cn"
        
        self.update_language_ui()

    def update_language_ui(self):
        # ดึงคำศัพท์จาก Dictionary มาใส่ปุ่ม
        t = self.texts[self.lang_code]
        
        self.logo_label.configure(text=t["title"])
        self.btn_add_file.configure(text=t["add_file"])
        self.btn_add_folder.configure(text=t["add_folder"])
        self.btn_clear.configure(text=t["clear"])
        self.btn_merge.configure(text=t["merge"])
        self.status_label.configure(text=t["status_ready"])

    # --- Dummy Functions (ยังไม่มีระบบรวมไฟล์จริง แค่เทสปุ่ม) ---
    def add_files_action(self):
        print("User clicked Add Files")
        
    def add_folder_action(self):
        print("User clicked Add Folder")
    
    def clear_action(self):
        print("User clicked Clear")
        
    def merge_action(self):
        print(f"Start Merging in language: {self.lang_code}")

if __name__ == "__main__":
    app = ExcelMergerApp()
    app.mainloop()