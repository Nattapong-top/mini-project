import customtkinter as ctk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
from PIL import Image
import os

# ---------------- Constants ----------------
class Config:
    MIN_FONT_SIZE = 20
    MAX_FONT_SIZE = 120
    DEFAULT_FONT_SIZE = 60
    MIN_OPACITY = 0.1
    MAX_OPACITY = 1.0
    DEFAULT_OPACITY = 0.5
    MIN_ROTATION = -180
    MAX_ROTATION = 180
    DEFAULT_ROTATION = 0
    PREVIEW_SCALE = 1.2
    DEBOUNCE_MS = 300

# ---------------- Base Dir ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class PDFWatermarkApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("PDF Watermark Tool - Professional Edition")
        self.geometry("1300x900")

        self.file_path = None
        self.preview_image = None
        self.preview_timer = None

        # Font paths with fallback
        self.font_map = {
            "TH": os.path.join(BASE_DIR, "fonts", "Sarabun-Regular.ttf"),
            "CN": os.path.join(BASE_DIR, "fonts", "NotoSansSC-Regular.ttf"),
            "EN": os.path.join(BASE_DIR, "fonts", "Arial.ttf"),
        }

        # Variables
        self.font_size_var = ctk.IntVar(value=Config.DEFAULT_FONT_SIZE)
        self.opacity_var = ctk.DoubleVar(value=Config.DEFAULT_OPACITY)
        self.rotation_var = ctk.IntVar(value=Config.DEFAULT_ROTATION)
        self.position_x_var = ctk.DoubleVar(value=0.5)  # 0-1 (center)
        self.position_y_var = ctk.DoubleVar(value=0.5)  # 0-1 (center)

        # Validate fonts on startup
        self.validate_fonts()

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=350)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

        self.main = ctk.CTkFrame(self)
        self.main.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")

        self.build_sidebar()
        self.build_main_area()

    # ---------------- Font Validation ----------------
    def validate_fonts(self):
        """Check if all font files exist"""
        missing = []
        for lang, path in self.font_map.items():
            if not os.path.exists(path):
                missing.append(f"  • {lang}: {os.path.basename(path)}")
        
        if missing:
            msg = "⚠️ ไม่พบไฟล์ฟอนต์:\n\n" + "\n".join(missing)
            msg += "\n\nโปรแกรมจะใช้ฟอนต์เริ่มต้นของระบบแทน"
            messagebox.showwarning("Font Files Missing", msg)

    # ---------------- UI - Sidebar ----------------
    def build_sidebar(self):
        # Header
        header = ctk.CTkLabel(
            self.sidebar,
            text="🔧 PDF WATERMARK",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        header.pack(pady=(20, 10))

        # File info frame
        self.file_info_frame = ctk.CTkFrame(self.sidebar)
        self.file_info_frame.pack(padx=15, pady=(0, 15), fill="x")
        
        self.file_label = ctk.CTkLabel(
            self.file_info_frame,
            text="📄 ยังไม่ได้เลือกไฟล์",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.file_label.pack(pady=10, padx=10)

        # Open PDF button
        ctk.CTkButton(
            self.sidebar,
            text="📂 เลือกไฟล์ PDF",
            command=self.open_pdf,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(padx=15, pady=(0, 20), fill="x")

        # Watermark text
        ctk.CTkLabel(
            self.sidebar,
            text="✍️ ข้อความลายน้ำ",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=(10, 5), padx=15, anchor="w")

        self.textbox = ctk.CTkTextbox(self.sidebar, height=100)
        self.textbox.pack(padx=15, fill="x")
        self.textbox.insert("1.0", "SAMPLE WATERMARK\nตัวอย่างลายน้ำ\n样本水印")

        # Enable right-click context menu on the actual text widget
        self.textbox._textbox.bind("<Button-3>", self.show_context_menu)
        
        # Bind keyboard shortcuts directly to the textbox widget
        self.textbox._textbox.bind("<Control-v>", lambda e: self.paste_text_event(e))
        self.textbox._textbox.bind("<Control-c>", lambda e: self.copy_text_event(e))
        self.textbox._textbox.bind("<Control-x>", lambda e: self.cut_text_event(e))
        self.textbox._textbox.bind("<Control-a>", lambda e: self.select_all_text_event(e))
        
        # Bind events for real-time update
        self.textbox.bind("<KeyRelease>", lambda e: self.schedule_preview_update())
        self.textbox.bind("<Return>", lambda e: self.schedule_preview_update())  # Enter key

        ctk.CTkButton(
            self.sidebar,
            text="🗑️ ล้างข้อความ",
            command=self.clear_text,
            fg_color="gray30",
            hover_color="gray20"
        ).pack(padx=15, pady=(8, 15), fill="x")

        # Font Size
        self.font_size_label_var = ctk.StringVar(value=f"{Config.DEFAULT_FONT_SIZE} pt")
        self.create_slider_with_value(
            "📏 ขนาดตัวอักษร",
            Config.MIN_FONT_SIZE,
            Config.MAX_FONT_SIZE,
            self.font_size_var,
            self.font_size_label_var
        )

        # Opacity
        self.opacity_label_var = ctk.StringVar(value=f"{int(Config.DEFAULT_OPACITY * 100)}%")
        self.create_slider_with_value(
            "💧 ความจาง (Opacity)",
            Config.MIN_OPACITY,
            Config.MAX_OPACITY,
            self.opacity_var,
            self.opacity_label_var,
            is_percentage=True
        )

        # Rotation
        self.rotation_label_var = ctk.StringVar(value=f"{Config.DEFAULT_ROTATION}°")
        self.create_slider_with_value(
            "🔄 มุมหมุน (Rotation)",
            Config.MIN_ROTATION,
            Config.MAX_ROTATION,
            self.rotation_var,
            self.rotation_label_var,
            is_degree=True
        )

        # Position controls
        ctk.CTkLabel(
            self.sidebar,
            text="📍 ตำแหน่งลายน้ำ",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=(20, 10), padx=15, anchor="w")

        # Position X
        self.position_x_label_var = ctk.StringVar(value="50%")
        self.create_slider_with_value(
            "← แนวนอน (X) →",
            0.0,
            1.0,
            self.position_x_var,
            self.position_x_label_var,
            is_percentage=True
        )

        # Position Y
        self.position_y_label_var = ctk.StringVar(value="50%")
        self.create_slider_with_value(
            "↑ แนวตั้ง (Y) ↓",
            0.0,
            1.0,
            self.position_y_var,
            self.position_y_label_var,
            is_percentage=True
        )

        # Save button
        ctk.CTkButton(
            self.sidebar,
            text="💾 บันทึก PDF",
            fg_color="#27ae60",
            hover_color="#229954",
            command=self.save_pdf,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(side="bottom", padx=15, pady=20, fill="x")

        # Reset button
        ctk.CTkButton(
            self.sidebar,
            text="↺ รีเซ็ตค่าเริ่มต้น",
            fg_color="gray30",
            hover_color="gray20",
            command=self.reset_settings
        ).pack(side="bottom", padx=15, pady=(0, 10), fill="x")

    def create_slider_with_value(self, label_text, from_, to, variable, display_var, is_percentage=False, is_degree=False):
        """Create a slider with value display"""
        frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        frame.pack(padx=15, pady=(15, 5), fill="x")

        # Label and value in same row
        label_frame = ctk.CTkFrame(frame, fg_color="transparent")
        label_frame.pack(fill="x")
        
        ctk.CTkLabel(
            label_frame,
            text=label_text,
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left")
        
        value_label = ctk.CTkLabel(
            label_frame,
            textvariable=display_var,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#3498db"
        )
        value_label.pack(side="right")

        # Slider
        def on_change(value):
            if is_percentage:
                display_var.set(f"{int(float(value) * 100)}%")
            elif is_degree:
                display_var.set(f"{int(float(value))}°")
            else:
                display_var.set(f"{int(float(value))} pt")
            self.schedule_preview_update()

        slider = ctk.CTkSlider(
            frame,
            from_=from_,
            to=to,
            variable=variable,
            command=on_change
        )
        slider.pack(fill="x", pady=(5, 0))

    # ---------------- UI - Main Area ----------------
    def build_main_area(self):
        # Title
        title = ctk.CTkLabel(
            self.main,
            text="📋 ตัวอย่างหน้าแรก (Preview)",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(10, 15))

        # Preview container with border
        preview_container = ctk.CTkFrame(self.main, fg_color="gray20")
        preview_container.pack(expand=True, fill="both", padx=20, pady=(0, 20))

        self.preview_label = ctk.CTkLabel(
            preview_container,
            text="👆 กรุณาเลือกไฟล์ PDF เพื่อดูตัวอย่าง\n\n📄 รองรับไฟล์ PDF ทุกขนาด",
            font=ctk.CTkFont(size=14),
            text_color="gray50"
        )
        self.preview_label.pack(expand=True, fill="both", padx=2, pady=2)

    # ---------------- Utilities ----------------
    def show_context_menu(self, event):
        """Show right-click context menu"""
        import tkinter as tk
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="ตัด (Cut)", command=self.cut_text, accelerator="Ctrl+X")
        menu.add_command(label="คัดลอก (Copy)", command=self.copy_text, accelerator="Ctrl+C")
        menu.add_command(label="วาง (Paste)", command=self.paste_text, accelerator="Ctrl+V")
        menu.add_separator()
        menu.add_command(label="เลือกทั้งหมด (Select All)", command=self.select_all_text, accelerator="Ctrl+A")
        menu.add_command(label="ลบทั้งหมด (Clear)", command=self.clear_text)
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def paste_text_event(self, event):
        """Handle paste with keyboard shortcut"""
        self.paste_text()
        return "break"
    
    def copy_text_event(self, event):
        """Handle copy with keyboard shortcut"""
        self.copy_text()
        return "break"
    
    def cut_text_event(self, event):
        """Handle cut with keyboard shortcut"""
        self.cut_text()
        return "break"
    
    def select_all_text_event(self, event):
        """Handle select all with keyboard shortcut"""
        self.select_all_text()
        return "break"
    
    def paste_text(self):
        """Handle paste operation"""
        try:
            clipboard_text = self.clipboard_get()
            text_widget = self.textbox._textbox
            
            # Delete selection if exists
            if text_widget.tag_ranges("sel"):
                text_widget.delete("sel.first", "sel.last")
            
            # Insert at cursor
            text_widget.insert("insert", clipboard_text)
            self.schedule_preview_update()
        except Exception as e:
            print(f"Paste error: {e}")
    
    def copy_text(self):
        """Handle copy operation"""
        try:
            text_widget = self.textbox._textbox
            if text_widget.tag_ranges("sel"):
                selected_text = text_widget.get("sel.first", "sel.last")
                self.clipboard_clear()
                self.clipboard_append(selected_text)
            else:
                # If nothing selected, copy all
                all_text = text_widget.get("1.0", "end-1c")
                self.clipboard_clear()
                self.clipboard_append(all_text)
        except Exception as e:
            print(f"Copy error: {e}")
    
    def cut_text(self):
        """Handle cut operation"""
        try:
            text_widget = self.textbox._textbox
            if text_widget.tag_ranges("sel"):
                selected_text = text_widget.get("sel.first", "sel.last")
                self.clipboard_clear()
                self.clipboard_append(selected_text)
                text_widget.delete("sel.first", "sel.last")
                self.schedule_preview_update()
        except Exception as e:
            print(f"Cut error: {e}")
    
    def select_all_text(self):
        """Handle select all operation"""
        try:
            text_widget = self.textbox._textbox
            text_widget.tag_add("sel", "1.0", "end-1c")
            text_widget.mark_set("insert", "end-1c")
            text_widget.see("insert")
            return "break"
        except Exception as e:
            print(f"Select all error: {e}")

    def clear_text(self):
        """Clear watermark text"""
        self.textbox.delete("1.0", "end")
        self.schedule_preview_update()

    def reset_settings(self):
        """Reset all settings to default"""
        self.font_size_var.set(Config.DEFAULT_FONT_SIZE)
        self.opacity_var.set(Config.DEFAULT_OPACITY)
        self.rotation_var.set(Config.DEFAULT_ROTATION)
        self.position_x_var.set(0.5)
        self.position_y_var.set(0.5)
        self.font_size_label_var.set(f"{Config.DEFAULT_FONT_SIZE} pt")
        self.opacity_label_var.set(f"{int(Config.DEFAULT_OPACITY * 100)}%")
        self.rotation_label_var.set(f"{Config.DEFAULT_ROTATION}°")
        self.position_x_label_var.set("50%")
        self.position_y_label_var.set("50%")
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", "SAMPLE WATERMARK\nตัวอย่างลายน้ำ\n样本水印")
        self.schedule_preview_update()

    def schedule_preview_update(self):
        """Debounced preview update to improve performance"""
        if self.preview_timer:
            self.after_cancel(self.preview_timer)
        self.preview_timer = self.after(Config.DEBOUNCE_MS, self.update_preview)

    def split_text_by_language(self, text):
        """Split text into lines, preserving newlines and spaces"""
        # Don't split by language anymore - keep everything together
        return [text]

    # ---------------- Watermark Application ----------------
    def apply_watermark(self, page):
        """Apply watermark to a PDF page with rotation support"""
        text = self.textbox.get("1.0", "end-1c")
        if not text.strip():
            return

        rect = page.rect
        
        # Use position variables (0-1 range)
        pos_x = self.position_x_var.get()
        pos_y = self.position_y_var.get()
        
        center_x = rect.width * pos_x
        center_y = rect.height * pos_y
        
        fontsize = self.font_size_var.get()
        opacity = self.opacity_var.get()
        rotation = self.rotation_var.get()
        color = (0.5, 0.5, 0.5)

        # Split text into lines
        lines = text.split('\n')
        
        # Calculate line spacing
        line_gap = fontsize * 1.4
        total_height = len(lines) * line_gap
        start_y = center_y - (total_height / 2)

        # Draw each line
        for idx, line in enumerate(lines):
            if line.strip():  # Skip empty lines but preserve spacing
                self._insert_rotated_text(
                    page, line,
                    center_x, start_y + idx * line_gap,
                    fontsize, color, opacity, rotation, rect
                )

    def _insert_rotated_text(self, page, text, x, y, fontsize, color, opacity, rotation, page_rect):
        """Insert text with rotation - supports multi-language in same line"""
        # Auto-detect and use appropriate font for mixed text
        # Try to find best font that supports the characters
        font = None
        font_file = None
        
        # Check if text contains Thai characters
        has_thai = any('\u0E00' <= ch <= '\u0E7F' for ch in text)
        # Check if text contains Chinese characters
        has_chinese = any('\u4E00' <= ch <= '\u9FFF' for ch in text)
        
        # Choose font based on content priority: Thai > Chinese > English
        if has_thai and os.path.exists(self.font_map["TH"]):
            font_file = self.font_map["TH"]
        elif has_chinese and os.path.exists(self.font_map["CN"]):
            font_file = self.font_map["CN"]
        elif os.path.exists(self.font_map["EN"]):
            font_file = self.font_map["EN"]
        
        # Create text writer
        tw = fitz.TextWriter(page_rect)
        
        # Load font
        if font_file:
            try:
                font = fitz.Font(fontfile=font_file)
            except:
                font = fitz.Font("helv")
        else:
            font = fitz.Font("helv")

        # Calculate text position
        text_length = font.text_length(text, fontsize=fontsize)
        
        # Position text - adjust Y for baseline
        pos = fitz.Point(x - text_length / 2, y + fontsize * 0.3)
        
        # Add text to writer
        tw.append(pos, text, font=font, fontsize=fontsize)

        # Create rotation matrix - rotate around text center
        center = fitz.Point(x, y)
        
        # Create transformation matrix (negate rotation for clockwise)
        mat = fitz.Matrix(1, 1)
        mat = mat.prerotate(-rotation)
        
        # Apply text with rotation and opacity
        tw.write_text(page, color=color, opacity=opacity, morph=(center, mat))

    # ---------------- Preview ----------------
    def update_preview(self):
        """Update the PDF preview"""
        if not self.file_path:
            return
        
        try:
            with fitz.open(self.file_path) as doc:
                if len(doc) == 0:
                    messagebox.showerror("ข้อผิดพลาด", "ไฟล์ PDF ไม่มีหน้าใดๆ")
                    return

                page = doc.load_page(0)
                self.apply_watermark(page)

                # Render with good quality
                pix = page.get_pixmap(matrix=fitz.Matrix(Config.PREVIEW_SCALE, Config.PREVIEW_SCALE))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                # Resize to fit preview area
                img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)

                self.preview_image = ctk.CTkImage(
                    light_image=img,
                    dark_image=img,
                    size=img.size
                )
                self.preview_label.configure(image=self.preview_image, text="")
                
        except Exception as e:
            error_msg = f"เกิดข้อผิดพลาดในการแสดงตัวอย่าง:\n{str(e)}"
            messagebox.showerror("Preview Error", error_msg)
            print(f"Preview error: {e}")

    # ---------------- File Operations ----------------
    def open_pdf(self):
        """Open PDF file dialog"""
        path = filedialog.askopenfilename(
            title="เลือกไฟล์ PDF",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        if path:
            self.file_path = path
            filename = os.path.basename(path)
            
            # Update file info
            self.file_label.configure(
                text=f"📄 {filename}",
                text_color="white"
            )
            
            self.update_preview()

    def save_pdf(self):
        """Save PDF with watermark"""
        if not self.file_path:
            messagebox.showwarning("⚠️ แจ้งเตือน", "กรุณาเลือกไฟล์ PDF ก่อน")
            return

        text = self.textbox.get("1.0", "end-1c")
        if not text.strip():
            result = messagebox.askyesno(
                "⚠️ ยืนยัน",
                "ไม่มีข้อความลายน้ำ\nต้องการบันทึกไฟล์โดยไม่มีลายน้ำใช่หรือไม่?"
            )
            if not result:
                return

        save_path = filedialog.asksaveasfilename(
            title="บันทึกไฟล์ PDF",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")],
            initialfile=f"watermarked_{os.path.basename(self.file_path)}"
        )
        
        if not save_path:
            return

        try:
            # Show processing message
            self.preview_label.configure(text="⏳ กำลังประมวลผล...\nโปรดรอสักครู่")
            self.update()

            with fitz.open(self.file_path) as doc:
                total_pages = len(doc)
                
                for page_num, page in enumerate(doc, 1):
                    self.apply_watermark(page)
                    
                    # Update progress
                    progress = int((page_num / total_pages) * 100)
                    self.preview_label.configure(
                        text=f"⏳ กำลังประมวลผล...\n\n📄 หน้า {page_num}/{total_pages} ({progress}%)"
                    )
                    self.update()
                
                doc.save(save_path)

            # Success message
            messagebox.showinfo(
                "✅ สำเร็จ",
                f"บันทึกไฟล์เรียบร้อยแล้ว!\n\n📁 {os.path.basename(save_path)}\n📄 จำนวน {total_pages} หน้า"
            )
            
            # Restore preview
            self.update_preview()

        except Exception as e:
            error_msg = f"เกิดข้อผิดพลาดในการบันทึก:\n\n{str(e)}"
            messagebox.showerror("❌ ข้อผิดพลาด", error_msg)
            print(f"Save error: {e}")
            
            # Restore preview
            if self.file_path:
                self.update_preview()


if __name__ == "__main__":
    app = PDFWatermarkApp()
    app.mainloop()