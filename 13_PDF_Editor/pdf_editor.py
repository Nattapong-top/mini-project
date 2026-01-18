import customtkinter as ctk
from tkinter import filedialog, messagebox, colorchooser
import fitz  # PyMuPDF
from PIL import Image
# 🔥 เพิ่ม numpy มาช่วยคำนวณการหมุน
import numpy as np
import matplotlib
# 🔥 สั่งให้ Matplotlib ทำงานเบื้องหลัง (กันบั๊กตีกับ GUI)
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure # 🔥 ใช้ Figure แทน plt.figure
import os
import io

# ---------------- Constants ----------------
class Config:
    MIN_FONT_SIZE = 5
    MAX_FONT_SIZE = 60 # 🛠️ ปรับเพิ่มเพดานให้หน่อย เผื่ออยากได้ตัวใหญ่มากๆ
    DEFAULT_FONT_SIZE = 20
    
    MIN_OPACITY = 0.1
    MAX_OPACITY = 1.0
    DEFAULT_OPACITY = 0.5
    
    MIN_ROTATION = -180
    MAX_ROTATION = 180
    DEFAULT_ROTATION = 30
    
    PREVIEW_SCALE = 1.2
    DEBOUNCE_MS = 300
    # 🛠️ ปรับเป็น 400 เพื่อความคมชัดระดับ HD
    WATERMARK_DPI = 400 
    DEFAULT_COLOR = "#505050"

# ---------------- Helper Functions ----------------
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    return (0.5, 0.5, 0.5)

# ---------------- Base Dir ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PDFWatermarkApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("PDF Watermark Tool - By Paa Top IT")
        self.geometry("1200x850") # ขนาดเริ่มต้น

        self.file_path = None
        self.preview_image = None
        self.preview_timer = None
        self.text_color = Config.DEFAULT_COLOR

        # Font setup
        self.font_map = {
            "TH": os.path.join(BASE_DIR, "fonts", "Sarabun-Regular.ttf"),
            "CN": os.path.join(BASE_DIR, "fonts", "NotoSansSC-Regular.ttf"),
            "EN": os.path.join(BASE_DIR, "fonts", "Arial.ttf"),
        }
        self.register_fonts()

        # Variables
        self.font_size_var = ctk.IntVar(value=Config.DEFAULT_FONT_SIZE)
        self.opacity_var = ctk.DoubleVar(value=Config.DEFAULT_OPACITY)
        self.rotation_var = ctk.IntVar(value=Config.DEFAULT_ROTATION)
        self.position_x_var = ctk.DoubleVar(value=0.5)
        self.position_y_var = ctk.DoubleVar(value=0.5)

        # Layout Main Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar Container (โครงสร้างหลัก) ---
        # แบ่งเป็น 2 ส่วน: บน(เลื่อนได้) กับ ล่าง(ปุ่ม Save ลอย)
        self.sidebar_container = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar_container.grid(row=0, column=0, sticky="nsew")
        
        self.sidebar_container.grid_rowconfigure(0, weight=1) # ส่วนบนขยายได้
        self.sidebar_container.grid_rowconfigure(1, weight=0) # ส่วนล่าง(Footer) ไม่ขยาย

        # 1. Scrollable Settings (ส่วนตั้งค่าแบบสวยงาม เลื่อนได้)
        self.settings_frame = ctk.CTkScrollableFrame(self.sidebar_container, width=300, label_text="⚙️ ตั้งค่า (Settings)", fg_color="transparent")
        self.settings_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # 2. Footer Actions (ปุ่มบันทึก ติดขอบล่างเสมอ)
        self.footer_frame = ctk.CTkFrame(self.sidebar_container, fg_color="#2b2b2b", corner_radius=0) # ใส่สีพื้นหลังให้ Footer ตัดกับส่วนบนนิดหน่อย
        self.footer_frame.grid(row=1, column=0, sticky="ew", padx=0, pady=0)

        # --- Main Preview Area ---
        self.main = ctk.CTkFrame(self)
        self.main.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")

        self.build_sidebar_content() # สร้างเนื้อหาสวยๆ ข้างบน
        self.build_footer_buttons()  # สร้างปุ่มล็อกข้างล่าง
        self.build_main_area()

    def register_fonts(self):
        self.registered_fonts = {}
        for lang, path in self.font_map.items():
            if os.path.exists(path):
                try:
                    fm.fontManager.addfont(path)
                    prop = fm.FontProperties(fname=path)
                    self.registered_fonts[lang] = prop.get_name()
                except: self.registered_fonts[lang] = None
            else: self.registered_fonts[lang] = None

    def show_context_menu(self, event):
        import tkinter as tk
        menu = tk.Menu(self, tearoff=0)
        widget = event.widget
        menu.add_command(label="Cut", command=lambda: widget.event_generate("<<Cut>>"))
        menu.add_command(label="Copy", command=lambda: widget.event_generate("<<Copy>>"))
        menu.add_command(label="Paste", command=lambda: widget.event_generate("<<Paste>>"))
        try: menu.tk_popup(event.x_root, event.y_root)
        finally: menu.grab_release()

    # ---------------- UI Construction (The Beautiful Part) ----------------
    def build_sidebar_content(self):
        parent = self.settings_frame
        
        # 1. Section: File
        self.add_section_header(parent, "📁 ไฟล์และเนื้อหา")
        self.file_label = ctk.CTkLabel(parent, text="ยังไม่ได้เลือกไฟล์", font=ctk.CTkFont(size=12), text_color="gray")
        self.file_label.pack(pady=(0, 5))
        ctk.CTkButton(parent, text="📂 เลือกไฟล์ PDF", command=self.open_pdf, height=35, fg_color="#3498db", hover_color="#2980b9").pack(padx=10, pady=(0, 10), fill="x")

        # Presets Area
        ctk.CTkLabel(parent, text="⚡ ข้อความด่วน", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10)
        preset_frame = ctk.CTkFrame(parent, fg_color="transparent")
        preset_frame.pack(padx=5, pady=(5, 10), fill="x")
        
        # Row 1: English
        row1 = ctk.CTkFrame(preset_frame, fg_color="transparent")
        row1.pack(fill="x", pady=2)
        self.create_preset_btn(row1, "DRAFT", "EN", "DRAFT COPY", "#2980b9", "#1f618d")
        self.create_preset_btn(row1, "CONFIDENTIAL", "EN", "CONFIDENTIAL", "#2980b9", "#1f618d")
        
        # Row 2: Thai
        row2 = ctk.CTkFrame(preset_frame, fg_color="transparent")
        row2.pack(fill="x", pady=2)
        self.create_preset_btn(row2, "สำเนาถูกต้อง", "TH", "สำเนาถูกต้อง", "#e67e22", "#d35400")
        self.create_preset_btn(row2, "เอกสารลับ", "TH", "เอกสารลับ ห้ามเผยแพร่", "#e67e22", "#d35400")

        # Row 3: Chinese
        row3 = ctk.CTkFrame(preset_frame, fg_color="transparent")
        row3.pack(fill="x", pady=2)
        self.create_preset_btn(row3, "绝密 (ลับที่สุด)", "CN", "绝密", "#c0392b", "#922b21")
        self.create_preset_btn(row3, "样本 (ตัวอย่าง)", "CN", "样本", "#c0392b", "#922b21")

        # Input Fields (Beautiful Style)
        input_container = ctk.CTkFrame(parent, fg_color="transparent")
        input_container.pack(padx=5, fill="x", pady=5)
        self.text_th = self.create_styled_input(input_container, "🇹🇭 ไทย")
        self.text_cn = self.create_styled_input(input_container, "🇨🇳 จีน")
        self.text_en = self.create_styled_input(input_container, "🇬🇧 อังกฤษ")

        # Tools Row
        tool_row = ctk.CTkFrame(parent, fg_color="transparent")
        tool_row.pack(fill="x", padx=10, pady=(10, 5))
        ctk.CTkButton(tool_row, text="🗑️ ล้างข้อความ", command=self.clear_text, fg_color="gray30", hover_color="gray20", width=100).pack(side="left")
        
        color_btn_frame = ctk.CTkFrame(tool_row, fg_color="transparent")
        color_btn_frame.pack(side="right")
        self.color_preview = ctk.CTkLabel(color_btn_frame, text="", width=25, height=25, fg_color=self.text_color, corner_radius=5)
        self.color_preview.pack(side="left", padx=(0, 5))
        ctk.CTkButton(color_btn_frame, text="🎨 สี", width=60, command=self.choose_color, fg_color="#8e44ad", hover_color="#71368a").pack(side="left")

        self.add_separator(parent)

        # 2. Section: Style
        self.add_section_header(parent, "🎨 รูปร่าง (Style)")
        
        self.font_size_label_var = ctk.StringVar(value=f"{Config.DEFAULT_FONT_SIZE}")
        self.create_slider(parent, "📏 ขนาด", Config.MIN_FONT_SIZE, Config.MAX_FONT_SIZE, self.font_size_var, self.font_size_label_var)

        self.opacity_label_var = ctk.StringVar(value=f"{int(Config.DEFAULT_OPACITY * 100)}%")
        self.create_slider(parent, "💧 ความจาง", Config.MIN_OPACITY, Config.MAX_OPACITY, self.opacity_var, self.opacity_label_var, is_percentage=True)

        self.rotation_label_var = ctk.StringVar(value=f"{Config.DEFAULT_ROTATION}°")
        self.create_slider(parent, "🔄 มุมหมุน", Config.MIN_ROTATION, Config.MAX_ROTATION, self.rotation_var, self.rotation_label_var, is_degree=True)

        self.add_separator(parent)

        # 3. Section: Position
        self.add_section_header(parent, "📍 ตำแหน่ง (Position)")
        
        self.position_x_label_var = ctk.StringVar(value="50%")
        self.create_slider(parent, "↔️ แนวนอน (X)", 0.0, 1.0, self.position_x_var, self.position_x_label_var, is_percentage=True)
        
        self.position_y_label_var = ctk.StringVar(value="50%")
        self.create_slider(parent, "↕️ แนวตั้ง (Y)", 0.0, 1.0, self.position_y_var, self.position_y_label_var, is_percentage=True)

    def build_footer_buttons(self):
        # พื้นที่ปุ่มล็อกตายตัวด้านล่าง (Locked Footer)
        # ใส่ Padding ให้ดูดี ไม่ชิดขอบจอเกินไป
        frame = ctk.CTkFrame(self.footer_frame, fg_color="transparent")
        frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkButton(frame, text="💾 บันทึก PDF (Save)", fg_color="#27ae60", hover_color="#219150", command=self.save_pdf, height=45, font=ctk.CTkFont(size=16, weight="bold")).pack(side="top", fill="x", pady=(0, 5))
        ctk.CTkButton(frame, text="↺ รีเซ็ตค่า (Reset)", fg_color="gray30", hover_color="gray20", command=self.reset_settings, height=30).pack(side="bottom", fill="x")

    def build_main_area(self):
        self.preview_container = ctk.CTkFrame(self.main, fg_color="#2b2b2b")
        self.preview_container.pack(expand=True, fill="both", padx=15, pady=15)
        self.preview_label = ctk.CTkLabel(self.preview_container, text="ตัวอย่างเอกสาร (Preview)", font=ctk.CTkFont(size=16), text_color="gray50")
        self.preview_label.pack(expand=True, fill="both")

    # --- UI Components Helpers ---
    def add_section_header(self, parent, text):
        ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=14, weight="bold"), text_color="#bdc3c7").pack(anchor="w", padx=10, pady=(15, 10))

    def add_separator(self, parent):
        ctk.CTkFrame(parent, height=2, fg_color="gray30").pack(fill="x", padx=10, pady=15)

    def create_preset_btn(self, parent, label, lang, text, color=None, hover=None):
        kwargs = {"height": 28, "command": lambda: self.apply_preset(lang, text)}
        if color: kwargs["fg_color"] = color
        if hover: kwargs["hover_color"] = hover
        ctk.CTkButton(parent, text=label, font=ctk.CTkFont(size=11), **kwargs).pack(side="left", padx=2, pady=0, expand=True, fill="x")

    def create_styled_input(self, parent, label):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=3)
        ctk.CTkLabel(frame, text=label, width=80, anchor="w", font=ctk.CTkFont(size=12)).pack(side="left", padx=(5,0))
        entry = ctk.CTkEntry(frame, height=30)
        entry.pack(side="left", fill="x", expand=True, padx=(0,5))
        entry.bind("<KeyRelease>", lambda e: self.schedule_preview_update())
        entry.bind("<Button-3>", self.show_context_menu)
        return entry

    def create_slider(self, parent, label_text, from_, to, variable, display_var, is_percentage=False, is_degree=False):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(padx=10, pady=0, fill="x")
        
        lbl_frame = ctk.CTkFrame(frame, fg_color="transparent")
        lbl_frame.pack(fill="x", pady=(5,0))
        ctk.CTkLabel(lbl_frame, text=label_text, font=ctk.CTkFont(size=12)).pack(side="left")
        ctk.CTkLabel(lbl_frame, textvariable=display_var, font=ctk.CTkFont(size=12, weight="bold"), text_color="#3498db").pack(side="right")
        
        def on_change(value):
            if is_percentage: display_var.set(f"{int(float(value) * 100)}%")
            elif is_degree: display_var.set(f"{int(float(value))}°")
            else: display_var.set(f"{int(float(value))}")
            self.schedule_preview_update()

        ctk.CTkSlider(frame, from_=from_, to=to, variable=variable, command=on_change, height=18).pack(fill="x", pady=(5, 5))

    # ---------------- Logic ----------------
    def choose_color(self):
        color = colorchooser.askcolor(initialcolor=self.text_color, title="เลือกสี")
        if color[1]:
            self.text_color = color[1]
            self.color_preview.configure(fg_color=self.text_color)
            self.schedule_preview_update()

    def apply_preset(self, lang, text):
        target = None
        if lang == "TH": target = self.text_th
        elif lang == "CN": target = self.text_cn
        elif lang == "EN": target = self.text_en
        
        if target:
            target.delete(0, "end")
            target.insert(0, text)
            self.schedule_preview_update()

    def clear_text(self):
        self.text_th.delete(0, "end")
        self.text_cn.delete(0, "end")
        self.text_en.delete(0, "end")
        self.schedule_preview_update()

    def reset_settings(self):
        self.font_size_var.set(Config.DEFAULT_FONT_SIZE)
        self.opacity_var.set(Config.DEFAULT_OPACITY)
        self.rotation_var.set(Config.DEFAULT_ROTATION)
        self.position_x_var.set(0.5)
        self.position_y_var.set(0.5)
        self.font_size_label_var.set(f"{Config.DEFAULT_FONT_SIZE}")
        self.opacity_label_var.set(f"{int(Config.DEFAULT_OPACITY * 100)}%")
        self.rotation_label_var.set(f"{Config.DEFAULT_ROTATION}°")
        self.position_x_label_var.set("50%")
        self.position_y_label_var.set("50%")
        self.text_color = Config.DEFAULT_COLOR
        self.color_preview.configure(fg_color=self.text_color)
        self.clear_text()
        self.text_th.insert(0, "ตัวอย่าง")
        self.schedule_preview_update()

    def schedule_preview_update(self):
        if self.preview_timer: self.after_cancel(self.preview_timer)
        self.preview_timer = self.after(Config.DEBOUNCE_MS, self.update_preview)

    def create_watermark_image_matplotlib(self, page_width, page_height):
        texts = [
            {"text": self.text_th.get(), "lang": "TH"},
            {"text": self.text_cn.get(), "lang": "CN"},
            {"text": self.text_en.get(), "lang": "EN"},
        ]
        active_texts = [t for t in texts if t["text"].strip()]
        if not active_texts: return None

        # ดึงค่าจากตัวแปร
        raw_fontsize = self.font_size_var.get() # ค่าที่ป๋าเลือกจาก Slider
        opacity = self.opacity_var.get()
        rotation = self.rotation_var.get()
        pos_x = self.position_x_var.get()
        pos_y = self.position_y_var.get()
        
        rgb_color = hex_to_rgb(self.text_color)
        final_color = (rgb_color[0], rgb_color[1], rgb_color[2], opacity)

        # 🔥 จุดสำคัญ: คำนวณขนาดฟอนต์ใหม่ให้สัมพันธ์กับ DPI
        # สูตร: ขนาดจริง = (ขนาดที่เลือก * 72) / DPI 
        # เพื่อให้ขนาด 20 pt บน 400 DPI ดูเท่ากับ 20 pt มาตรฐาน
        fontsize = (raw_fontsize * 72) / Config.WATERMARK_DPI
        
        # 🔥 ใช้ค่า DPI ใหม่ (400)
        # 🔥 ใช้ Figure() (OO Style) แทน plt.figure() เพื่อกัน Memory Leak
        fig = Figure(figsize=(page_width / Config.WATERMARK_DPI, page_height / Config.WATERMARK_DPI), dpi=Config.WATERMARK_DPI)
        fig.patch.set_alpha(0)
        ax = fig.add_subplot(111)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
        
        # 🔥 สูตรคำนวณระยะห่างใหม่ ป้องกันการทับกันเวลาหมุน
        pixel_height = (fontsize / 72) * Config.WATERMARK_DPI
        base_spacing = (pixel_height / page_height) * 1.3
        rotation_factor = 1.0 + abs(np.sin(np.radians(rotation))) * 0.8
        line_spacing = base_spacing * rotation_factor

        for i, item in enumerate(active_texts):
            font_name = 'sans-serif'
            if item["lang"] == "TH" and self.registered_fonts.get("TH"): font_name = self.registered_fonts["TH"]
            elif item["lang"] == "CN" and self.registered_fonts.get("CN"): font_name = self.registered_fonts["CN"]
            elif item["lang"] == "EN" and self.registered_fonts.get("EN"): font_name = self.registered_fonts["EN"]
            
            offset_index = i - (len(active_texts) - 1) / 2
            current_y_offset = -offset_index * line_spacing

            ax.text(pos_x, pos_y + current_y_offset, item["text"],
                    fontsize=fontsize, fontname=font_name, color=final_color,
                    ha='center', va='center', rotation=rotation, transform=ax.transAxes)
        
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        buf = canvas.buffer_rgba()
        w, h = canvas.get_width_height()
        watermark = Image.frombytes('RGBA', (w, h), buf)
        # ไม่ต้อง plt.close(fig) แล้วเพราะใช้ Object Oriented
        return watermark

    def update_preview(self):
        if not self.file_path: return
        try:
            # 🛑 1. ทำลาย (Destroy) Label ตัวเก่าทิ้งไปเลย เพื่อป้องกัน "pyimage doesn't exist"
            if hasattr(self, 'preview_label'):
                self.preview_label.destroy()

            # 🛑 2. ล้างตัวแปรเก็บรูปเก่าให้เกลี้ยง
            self.preview_image = None
            
            with fitz.open(self.file_path) as doc:
                if len(doc) == 0: return
                page = doc.load_page(0)
                
                # สร้างลายน้ำ (ใส้ในที่ป๋าปรับไว้)
                watermark = self.create_watermark_image_matplotlib(page.rect.width, page.rect.height)
                if watermark:
                    img_buffer = io.BytesIO()
                    watermark.save(img_buffer, format='PNG')
                    page.insert_image(page.rect, stream=img_buffer.getvalue(), overlay=True)

                # Render PDF หน้าแรก
                pix = page.get_pixmap(matrix=fitz.Matrix(Config.PREVIEW_SCALE, Config.PREVIEW_SCALE))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                container_width = self.preview_container.winfo_width()
                container_height = self.preview_container.winfo_height()
                if container_width > 50 and container_height > 50:
                     img.thumbnail((container_width - 10, container_height - 10), Image.Resampling.LANCZOS)

                # 🛑 3. สร้างรูปใหม่เก็บไว้ในตัวแปร self
                self.preview_image = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)

                # 🛑 4. สร้าง Label ตัวใหม่ขึ้นมาสดๆ ร้อนๆ แล้ววางลงใน container เดิม
                self.preview_label = ctk.CTkLabel(self.preview_container, image=self.preview_image, text="")
                self.preview_label.pack(expand=True, fill="both")
                
        except Exception as e: 
            print(f"Preview error: {e}")

    def open_pdf(self):
        path = filedialog.askopenfilename(title="เลือกไฟล์ PDF", filetypes=[("PDF Files", "*.pdf")])
        if path:
            self.file_path = path
            self.file_label.configure(text=f"📄 {os.path.basename(path)}", text_color="white")
            self.update_preview()

    def save_pdf(self):
        if not self.file_path: return messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกไฟล์ PDF ก่อน")
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")], initialfile=f"watermarked_{os.path.basename(self.file_path)}")
        if not save_path: return

        try:
            self.preview_label.configure(text="⏳ กำลังประมวลผล...", image=None)
            self.update()
            with fitz.open(self.file_path) as doc:
                for page in doc:
                    watermark = self.create_watermark_image_matplotlib(page.rect.width, page.rect.height)
                    if watermark:
                        img_buffer = io.BytesIO()
                        watermark.save(img_buffer, format='PNG')
                        page.insert_image(page.rect, stream=img_buffer.getvalue(), overlay=True)
                doc.save(save_path)
            messagebox.showinfo("สำเร็จ", f"บันทึกเรียบร้อย!\n{os.path.basename(save_path)}")
            self.update_preview()
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", str(e))
            self.update_preview()

if __name__ == "__main__":
    app = PDFWatermarkApp()
    app.mainloop()