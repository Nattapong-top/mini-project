import customtkinter as ctk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
from PIL import Image
import os

# ---------------- Base Dir ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------- Theme -------------------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class PDFWatermarkApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("PDF Watermark Tool")
        self.geometry("1200x850")

        # ---------- State ----------
        self.file_path = None
        self.preview_image = None

        self.font_map = {
            "TH": os.path.join(BASE_DIR, "fonts", "Sarabun-Regular.ttf"),
            "EN": os.path.join(BASE_DIR, "fonts", "Arial.ttf"),
            "CN": os.path.join(BASE_DIR, "fonts", "NotoSansSC-Regular.ttf"),
        }

        self.rotate_var = ctk.DoubleVar(value=45)
        self.font_size_var = ctk.IntVar(value=60)

        # ---------- Layout ----------
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=320)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.main = ctk.CTkFrame(self)
        self.main.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.build_sidebar()

        self.preview_label = ctk.CTkLabel(
            self.main, text="ยังไม่ได้เลือกไฟล์ PDF"
        )
        self.preview_label.pack(expand=True, fill="both")

    # ---------- Sidebar ----------
    def build_sidebar(self):
        ctk.CTkLabel(
            self.sidebar,
            text="PDF WATERMARK",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=20)

        ctk.CTkButton(
            self.sidebar, text="เลือกไฟล์ PDF",
            command=self.open_pdf
        ).pack(padx=20, fill="x")

        # ---- Textbox ----
        ctk.CTkLabel(self.sidebar, text="ข้อความลายน้ำ").pack(pady=(20, 5))
        self.textbox = ctk.CTkTextbox(self.sidebar, height=120)
        self.textbox.pack(padx=20, fill="x")

        # Enable Copy / Paste / Cut
        self.textbox.bind("<Control-v>", lambda e: self.textbox.event_generate("<<Paste>>"))
        self.textbox.bind("<Control-c>", lambda e: self.textbox.event_generate("<<Copy>>"))
        self.textbox.bind("<Control-x>", lambda e: self.textbox.event_generate("<<Cut>>"))
        self.textbox.bind("<KeyRelease>", lambda e: self.update_preview())

        # ---- Clear Button ----
        ctk.CTkButton(
            self.sidebar,
            text="ล้างข้อความ",
            fg_color="#555555",
            command=self.clear_text
        ).pack(padx=20, pady=8, fill="x")

        # ---- Font Size ----
        ctk.CTkLabel(self.sidebar, text="ขนาดตัวอักษร").pack(pady=(15, 5))
        ctk.CTkSlider(
            self.sidebar,
            from_=20,
            to=120,
            variable=self.font_size_var,
            command=lambda _: self.update_preview(),
        ).pack(padx=20, fill="x")

        # ---- Opacity ----
        ctk.CTkLabel(self.sidebar, text="ความจาง (Opacity)").pack(pady=(15, 5))
        self.opacity = ctk.CTkSlider(
            self.sidebar,
            from_=0.1,
            to=1.0,
            command=lambda _: self.update_preview(),
        )
        self.opacity.set(0.5)
        self.opacity.pack(padx=20, fill="x")

        # ---- Rotate ----
        ctk.CTkLabel(self.sidebar, text="องศา (Rotate)").pack(pady=(15, 5))
        ctk.CTkSlider(
            self.sidebar,
            from_=-90,
            to=90,
            variable=self.rotate_var,
            command=lambda _: self.update_preview(),
        ).pack(padx=20, fill="x")

        # ---- Save ----
        ctk.CTkButton(
            self.sidebar,
            text="บันทึก PDF",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=self.save_pdf,
        ).pack(side="bottom", padx=20, pady=30, fill="x")

    # ---------- Utilities ----------
    def clear_text(self):
        self.textbox.delete("1.0", "end")
        self.update_preview()

    def detect_font(self, text):
        for ch in text:
            if '\u4e00' <= ch <= '\u9fff':
                return self.font_map["CN"]
            if '\u0E00' <= ch <= '\u0E7F':
                return self.font_map["TH"]
        return self.font_map["EN"]

    def ensure_font(self, page, fontname, fontfile):
        if fontname not in page.get_fonts():
            page.insert_font(fontname=fontname, fontfile=fontfile)

   

    # ---------- Watermark Engine ----------
    def apply_watermark(self, page):
        text = self.textbox.get("1.0", "end-1c").strip()
        if not text:
            return

        font_path = self.detect_font(text)
        if not os.path.exists(font_path):
            return

        # ตั้งชื่อฟอนต์ตามภาษา (สำคัญ)
        if font_path.endswith("Sarabun-Regular.ttf"):
            fontname = "TH_FONT"
        elif font_path.endswith("NotoSansSC-Regular.ttf"):
            fontname = "CN_FONT"
        else:
            fontname = "EN_FONT"

        # ✅ register ฟอนต์ก่อน (หัวใจของปัญหานี้)
        self.ensure_font(page, fontname, font_path)

        rect = page.rect
        text_rect = fitz.Rect(
            rect.width * 0.05,
            rect.height * 0.25,
            rect.width * 0.95,
            rect.height * 0.75
        )

        page.insert_textbox(
            text_rect,
            text,
            fontsize=self.font_size_var.get(),
            fontname=fontname,     # << ใช้ชื่อที่ register แล้ว
            color=(0.5, 0.5, 0.5),
            fill_opacity=self.opacity.get(),
            align=fitz.TEXT_ALIGN_CENTER,
            rotate=0
        )



    # ---------- Preview ----------
    def update_preview(self):
        if not self.file_path:
            return
        try:
            with fitz.open(self.file_path) as doc:
                page = doc.load_page(0)
                self.apply_watermark(page)

                pix = page.get_pixmap(matrix=fitz.Matrix(1.2, 1.2))
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img.thumbnail((900, 900))

                self.preview_image = ctk.CTkImage(
                    light_image=img,
                    dark_image=img,
                    size=img.size,
                )
                self.preview_label.configure(image=self.preview_image, text="")
        except Exception as e:
            print("Preview error:", e)

    # ---------- Actions ----------
    def open_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
        if path:
            self.file_path = path
            self.update_preview()

    def save_pdf(self):
        if not self.file_path:
            messagebox.showwarning("แจ้งเตือน", "ยังไม่ได้เลือกไฟล์")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
        )
        if not save_path:
            return

        with fitz.open(self.file_path) as doc:
            for page in doc:
                self.apply_watermark(page)
            doc.save(save_path)

        messagebox.showinfo("สำเร็จ", "บันทึกไฟล์เรียบร้อยแล้ว")


if __name__ == "__main__":
    app = PDFWatermarkApp()
    app.mainloop()
