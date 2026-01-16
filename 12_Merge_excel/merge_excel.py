import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
import os
import platform
import subprocess

# ตั้งค่าธีม
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ExcelMergerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 1. ตั้งค่าตัวแปร ---
        self.all_file_paths = []
        self.last_save_path = "" # เพิ่มตัวแปรจำที่อยู่ไฟล์ล่าสุด
        self.lang_code = "en"

        # --- 2. ข้อมูลภาษา (เพิ่มคำศัพท์ปุ่มเปิดโฟลเดอร์) ---
        self.texts = {
            "en": {
                "title": "Excel Merger Tool",
                "add_file": "Add Files",
                "add_folder": "Add Folder",
                "clear": "Clear List",
                "merge": "MERGE FILES",
                "open_dir": "Open Folder", # <--- เพิ่ม
                "status_ready": "Ready...",
                "status_done": "Done! Saved at:",
                "status_error": "Error: ",
                "msg_no_file": "Please select files first!",
                "msg_success": "Success!",
                "lang_label": "Language:"
            },
            "th": {
                "title": "โปรแกรมรวมไฟล์ Excel",
                "add_file": "เพิ่มไฟล์",
                "add_folder": "เพิ่มโฟลเดอร์",
                "clear": "ล้างรายการ",
                "merge": "เริ่มรวมไฟล์",
                "open_dir": "เปิดโฟลเดอร์เก็บไฟล์", # <--- เพิ่ม
                "status_ready": "พร้อมทำงาน...",
                "status_done": "เรียบร้อย! บันทึกที่:",
                "status_error": "เกิดข้อผิดพลาด: ",
                "msg_no_file": "กรุณาเลือกไฟล์ก่อนครับ!",
                "msg_success": "เรียบร้อย!",
                "lang_label": "ภาษา:"
            },
            "cn": {
                "title": "Excel 合并工具",
                "add_file": "添加文件",
                "add_folder": "添加文件夹",
                "clear": "清空列表",
                "merge": "立即合并",
                "open_dir": "打开文件夹", # <--- เพิ่ม
                "status_ready": "准备就绪...",
                "status_done": "合并完成！保存于：",
                "status_error": "错误：",
                "msg_no_file": "请先选择文件！",
                "msg_success": "成功！",
                "lang_label": "语言:"
            }
        }

        # --- 3. สร้างหน้าตา ---
        self.title("Excel Merger Pro - By Paa Top IT")
        self.geometry("750x600") # ขยายความสูงนิดหน่อยเผื่อปุ่มใหม่
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_widgets()
        self.update_language_ui()

    def create_widgets(self):
        # Header Bar
        self.header_frame = ctk.CTkFrame(self, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        
        self.logo_label = ctk.CTkLabel(self.header_frame, text="Excel Merger", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(side="left", padx=20, pady=15)

        self.lang_option = ctk.CTkOptionMenu(self.header_frame, values=["English", "ไทย", "中文"], command=self.change_language_event, width=100)
        self.lang_option.pack(side="right", padx=20, pady=10)
        self.lang_label_ui = ctk.CTkLabel(self.header_frame, text="Language:")
        self.lang_label_ui.pack(side="right", padx=5)

        # Main Content
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # File List
        self.file_list_display = ctk.CTkTextbox(self.main_frame, font=("Consolas", 14))
        self.file_list_display.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        self.file_list_display.insert("0.0", "Please add files...\n")
        self.file_list_display.configure(state="disabled")

        # Buttons
        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.grid(row=0, column=1, sticky="ns")

        self.btn_add_file = ctk.CTkButton(self.btn_frame, text="Add Files", command=self.add_files_action)
        self.btn_add_file.pack(pady=(0, 10), fill="x")

        self.btn_add_folder = ctk.CTkButton(self.btn_frame, text="Add Folder", command=self.add_folder_action)
        self.btn_add_folder.pack(pady=(0, 10), fill="x")

        self.btn_clear = ctk.CTkButton(self.btn_frame, text="Clear", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.clear_action)
        self.btn_clear.pack(pady=(0, 20), fill="x")

        self.btn_merge = ctk.CTkButton(self.btn_frame, text="MERGE", height=60, fg_color="#2CC985", hover_color="#229965", font=ctk.CTkFont(size=16, weight="bold"), command=self.merge_action)
        self.btn_merge.pack(side="bottom", fill="x", pady=(10, 0))

        # --- เพิ่มปุ่ม Open Folder ---
        # วางไว้เหนือปุ่ม Merge หรือ ใต้ปุ่ม Merge ก็ได้ (อันนี้วางไว้ข้างบน Merge นิดนึง)
        self.btn_open_folder = ctk.CTkButton(self.btn_frame, text="Open Folder", fg_color="#3B8ED0", command=self.open_folder_action)
        self.btn_open_folder.pack(side="bottom", fill="x", pady=(0, 10)) 
        self.btn_open_folder.configure(state="disabled") # เริ่มต้นห้ามกด จนกว่าจะรวมเสร็จ

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="Ready...", anchor="w", text_color="gray")
        self.status_label.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))

    # --- 4. Logic ---

    def update_file_list_ui(self):
        self.file_list_display.configure(state="normal")
        self.file_list_display.delete("0.0", "end")
        if not self.all_file_paths:
            self.file_list_display.insert("0.0", "No files selected...\n")
        else:
            for path in self.all_file_paths:
                self.file_list_display.insert("end", f"📄 {os.path.basename(path)}\n")
        self.file_list_display.configure(state="disabled")

    def add_files_action(self):
        files = filedialog.askopenfilenames(filetypes=[("Excel Files", "*.xlsx *.xls")])
        if files:
            for f in files:
                if f not in self.all_file_paths:
                    self.all_file_paths.append(f)
            self.update_file_list_ui()

    def add_folder_action(self):
        folder = filedialog.askdirectory()
        if folder:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.endswith((".xlsx", ".xls")) and not file.startswith("~$"):
                        full_path = os.path.join(root, file)
                        if full_path not in self.all_file_paths:
                            self.all_file_paths.append(full_path)
            self.update_file_list_ui()

    def clear_action(self):
        self.all_file_paths = []
        self.last_save_path = "" # ล้าง path เก่าด้วย
        self.btn_open_folder.configure(state="disabled") # ปิดปุ่มเปิดโฟลเดอร์
        self.update_file_list_ui()
        self.status_label.configure(text=self.texts[self.lang_code]["status_ready"])

    def merge_action(self):
        t = self.texts[self.lang_code]
        if not self.all_file_paths:
            messagebox.showwarning("Warning", t["msg_no_file"])
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")], initialfile="Merged_Output.xlsx")
        if not save_path: return

        self.status_label.configure(text="Processing...")
        self.update()

        try:
            data_frames = []
            for file in self.all_file_paths:
                df = pd.read_excel(file)
                data_frames.append(df)
            
            result = pd.concat(data_frames, ignore_index=True)
            result.to_excel(save_path, index=False)
            
            # --- จำ Path และเปิดใช้งานปุ่ม ---
            self.last_save_path = save_path
            self.btn_open_folder.configure(state="normal") # ปลดล็อคปุ่ม
            
            self.status_label.configure(text=f"{t['status_done']} {os.path.basename(save_path)}")
            messagebox.showinfo(t["msg_success"], f"{t['msg_success']}\nSaved to: {save_path}")
            
        except Exception as e:
            self.status_label.configure(text=f"{t['status_error']} {str(e)}")
            messagebox.showerror("Error", f"{str(e)}")

    def open_folder_action(self):
        """Logic: เปิดโฟลเดอร์ที่เก็บไฟล์"""
        if self.last_save_path and os.path.exists(self.last_save_path):
            folder_path = os.path.dirname(self.last_save_path) # เอาแค่ชื่อโฟลเดอร์ ตัดชื่อไฟล์ออก
            
            # คำสั่งเปิดโฟลเดอร์ตาม OS (Windows/Mac/Linux)
            if platform.system() == "Windows":
                os.startfile(folder_path)
            elif platform.system() == "Darwin":  # Mac
                subprocess.Popen(["open", folder_path])
            else:  # Linux
                subprocess.Popen(["xdg-open", folder_path])
        else:
            print("Path not found!")

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
        self.btn_open_folder.configure(text=t["open_dir"]) # อัปเดตภาษาปุ่มใหม่
        
        if "Error" not in self.status_label.cget("text") and "Saved" not in self.status_label.cget("text"):
             self.status_label.configure(text=t["status_ready"])

if __name__ == "__main__":
    app = ExcelMergerApp()
    app.mainloop()