import customtkinter as ctk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
from PIL import Image, ImageTk

# ตั้งค่าธีม
ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("blue")

class PDFWatermarkerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PDF Watermarker By Paa Top IT")
        self.geometry("1200x850") 

        # --- Data State ---
        self.pdf_doc = None
        self.file_path = None
        self.preview_tk_image = None

        # --- Layout ---
        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=1)

        # 1. Sidebar
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False) 
        self.setup_sidebar()

        # 2. Main Content
        self.main_content = ctk.CTkFrame(self, corner_radius=15)
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.preview_label = ctk.CTkLabel(self.main_content, text="ยังไม่ได้เลือกไฟล์ PDF", font=("Sarabun", 18))
        self.preview_label.pack(expand=True, fill="both", padx=10, pady=10)

    def setup_sidebar(self):
        ctk.CTkLabel(self.sidebar, text="PDF EDITOR", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=30)

        self.btn_open = ctk.CTkButton(self.sidebar, text="📁 เลือกไฟล์ PDF", command=self.open_pdf, height=40)
        self.btn_open.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(self.sidebar, text="ข้อความลายน้ำ (พิมพ์หลายบรรทัด):", font=("Sarabun", 14)).pack(pady=(20, 0))
        self.entry_text = ctk.CTkTextbox(self.sidebar, height=200, corner_radius=10, border_width=2)
        self.entry_text.pack(pady=10, padx=20, fill="x")
        # เมื่อพิมพ์ หรือ ปล่อยปุ่ม ให้รีเฟรช Preview
        self.entry_text.bind("<KeyRelease>", lambda e: self.update_preview())

        ctk.CTkLabel(self.sidebar, text="ความเข้ม (Opacity):", font=("Sarabun", 14)).pack(pady=(10, 0))
        self.opacity_slider = ctk.CTkSlider(self.sidebar, from_=0.1, to=1.0, command=lambda v: self.update_preview())
        self.opacity_slider.set(0.5)
        self.opacity_slider.pack(pady=10, padx=20, fill="x")

        self.btn_clear = ctk.CTkButton(self.sidebar, text="ล้างข้อความ", fg_color="transparent", border_width=1, command=self.clear_text)
        self.btn_clear.pack(pady=10)

        self.btn_save = ctk.CTkButton(self.sidebar, text="💾 บันทึกไฟล์ (Watermarked)", 
                                      fg_color="#e74c3c", hover_color="#c0392b",
                                      command=self.save_pdf, height=45)
        self.btn_save.pack(side="bottom", pady=30, padx=20, fill="x")

    def open_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if path:
            try:
                self.file_path = path
                # โหลดไฟล์เข้าหน่วยความจำ
                self.pdf_doc = fitz.open(self.file_path)
                self.update_preview()
            except Exception as e:
                messagebox.showerror("Error", f"เปิดไฟล์ไม่ได้: {e}")

    def update_preview(self):
        """หัวใจหลัก: วาดลายน้ำจำลองลงบน Preview"""
        if not self.file_path: return

        try:
            # เปิดไฟล์แบบ Temporary เพื่อใช้ทำ Preview (ไม่ให้กระทบไฟล์หลัก)
            temp_doc = fitz.open(self.file_path)
            page = temp_doc.load_page(0)
            
            text = self.entry_text.get("1.0", "end-1c")
            opacity = self.opacity_slider.get()

            if text.strip():
                # จำลองการใส่ลายน้ำลงในหน้าแรกของ Temp Doc
                rect = page.rect
                text_rect = fitz.Rect(50, 50, rect.width - 50, rect.height - 50)
                page.insert_textbox(text_rect, text,
                                    fontsize=50,
                                    color=(0.7, 0.7, 0.7),
                                    fill_opacity=opacity,
                                    align=fitz.TEXT_ALIGN_CENTER,
                                    rotate=45)

            # แปลงหน้าที่ใส่ลายน้ำแล้วเป็นรูปภาพ
            pix = page.get_pixmap(matrix=fitz.Matrix(1.2, 1.2))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img.thumbnail((800, 800))
            
            self.preview_tk_image = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.preview_label.configure(image=self.preview_tk_image, text="")
            
            temp_doc.close() # ปิดไฟล์ชั่วคราว
        except Exception as e:
            print(f"Preview error: {e}")

    def clear_text(self):
        self.entry_text.delete("1.0", "end")
        self.update_preview()

    def save_pdf(self):
        if not self.file_path:
            messagebox.showwarning("คำเตือน", "เลือกไฟล์ก่อนครับป๋า!")
            return

        text = self.entry_text.get("1.0", "end-1c")
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        
        if save_path:
            with fitz.open(self.file_path) as output_doc:
                opacity = self.opacity_slider.get()
                for page in output_doc:
                    rect = page.rect
                    text_rect = fitz.Rect(50, 50, rect.width - 50, rect.height - 50)
                    page.insert_textbox(text_rect, text,
                                        fontsize=50,
                                        color=(0.7, 0.7, 0.7),
                                        fill_opacity=opacity,
                                        align=fitz.TEXT_ALIGN_CENTER,
                                        rotate=45)
                output_doc.save(save_path)
            messagebox.showinfo("สำเร็จ", "บันทึกไฟล์เรียบร้อยแล้วครับ!")

if __name__ == "__main__":
    app = PDFWatermarkerApp()
    app.mainloop()