import customtkinter as ctk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
from PIL import Image
import os

# ---------------- Base Dir ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class PDFWatermarkApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("PDF Watermark Tool")
        self.geometry("1200x850")

        self.file_path = None
        self.preview_image = None

        self.font_map = {
            "TH": os.path.join(BASE_DIR, "fonts", "Sarabun-Regular.ttf"),
            "CN": os.path.join(BASE_DIR, "fonts", "NotoSansSC-Regular.ttf"),
            "EN": os.path.join(BASE_DIR, "fonts", "Arial.ttf"),
        }

        self.font_size_var = ctk.IntVar(value=60)

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=320)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.main = ctk.CTkFrame(self)
        self.main.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.build_sidebar()

        self.preview_label = ctk.CTkLabel(self.main, text="ยังไม่ได้เลือกไฟล์ PDF")
        self.preview_label.pack(expand=True, fill="both")

    # ---------------- UI ----------------
    def build_sidebar(self):
        ctk.CTkLabel(
            self.sidebar, text="PDF WATERMARK",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        ctk.CTkButton(
            self.sidebar, text="เลือกไฟล์ PDF",
            command=self.open_pdf
        ).pack(padx=20, fill="x")

        ctk.CTkLabel(self.sidebar, text="ข้อความลายน้ำ").pack(pady=(20, 5))
        self.textbox = ctk.CTkTextbox(self.sidebar, height=120)
        self.textbox.pack(padx=20, fill="x")

        # copy / paste / cut
        self.textbox.bind("<Control-v>", lambda e: self.textbox.event_generate("<<Paste>>"))
        self.textbox.bind("<Control-c>", lambda e: self.textbox.event_generate("<<Copy>>"))
        self.textbox.bind("<Control-x>", lambda e: self.textbox.event_generate("<<Cut>>"))
        self.textbox.bind("<KeyRelease>", lambda e: self.update_preview())

        ctk.CTkButton(
            self.sidebar, text="ล้างข้อความ",
            command=self.clear_text
        ).pack(padx=20, pady=8, fill="x")

        ctk.CTkLabel(self.sidebar, text="ขนาดตัวอักษร").pack(pady=(15, 5))
        ctk.CTkSlider(
            self.sidebar, from_=20, to=120,
            variable=self.font_size_var,
            command=lambda _: self.update_preview()
        ).pack(padx=20, fill="x")

        ctk.CTkLabel(self.sidebar, text="ความจาง (Opacity)").pack(pady=(15, 5))
        self.opacity = ctk.CTkSlider(
            self.sidebar, from_=0.1, to=1.0,
            command=lambda _: self.update_preview()
        )
        self.opacity.set(0.5)
        self.opacity.pack(padx=20, fill="x")

        ctk.CTkButton(
            self.sidebar,
            text="บันทึก PDF",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=self.save_pdf
        ).pack(side="bottom", padx=20, pady=30, fill="x")

    # ---------------- Utilities ----------------
    def clear_text(self):
        self.textbox.delete("1.0", "end")
        self.update_preview()

    def split_text_by_language(self, text):
        thai = ""
        chinese = ""
        latin = ""

        for ch in text:
            if '\u0E00' <= ch <= '\u0E7F':
                thai += ch
            elif '\u4E00' <= ch <= '\u9FFF':
                chinese += ch
            else:
                latin += ch

        return thai.strip(), chinese.strip(), latin.strip()

    # ---------------- Watermark ----------------
    def apply_watermark(self, page):
        text = self.textbox.get("1.0", "end-1c").strip()
        if not text:
            return

        thai, chinese, latin = self.split_text_by_language(text)

        rect = page.rect
        center_y = rect.height * 0.5
        line_gap = self.font_size_var.get() * 1.2

        fontsize = self.font_size_var.get()
        opacity = self.opacity.get()
        color = (0.5, 0.5, 0.5)

        # นับว่ามีกี่ภาษา เพื่อจัดกึ่งกลางรวม
        blocks = [b for b in (thai, chinese, latin) if b]
        start_y = center_y - (len(blocks) - 1) * line_gap / 2

        idx = 0

        if thai:
            text_rect = fitz.Rect(
                rect.width * 0.05,
                start_y + idx * line_gap,
                rect.width * 0.95,
                start_y + idx * line_gap + fontsize * 2
            )
            page.insert_textbox(
                text_rect, thai,
                fontsize=fontsize,
                fontname="TH_FONT",
                fontfile=self.font_map["TH"],
                color=color,
                fill_opacity=opacity,
                align=fitz.TEXT_ALIGN_CENTER
            )
            idx += 1

        if chinese:
            text_rect = fitz.Rect(
                rect.width * 0.05,
                start_y + idx * line_gap,
                rect.width * 0.95,
                start_y + idx * line_gap + fontsize * 2
            )
            page.insert_textbox(
                text_rect, chinese,
                fontsize=fontsize,
                fontname="CN_FONT",
                fontfile=self.font_map["CN"],
                color=color,
                fill_opacity=opacity,
                align=fitz.TEXT_ALIGN_CENTER
            )
            idx += 1

        if latin:
            text_rect = fitz.Rect(
                rect.width * 0.05,
                start_y + idx * line_gap,
                rect.width * 0.95,
                start_y + idx * line_gap + fontsize * 2
            )
            page.insert_textbox(
                text_rect, latin,
                fontsize=fontsize,
                fontname="EN_FONT",
                fontfile=self.font_map["EN"],
                color=color,
                fill_opacity=opacity,
                align=fitz.TEXT_ALIGN_CENTER
            )


    # ---------------- Preview ----------------
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
                    size=img.size
                )
                self.preview_label.configure(image=self.preview_image, text="")
        except Exception as e:
            print("Preview error:", e)

    # ---------------- Actions ----------------
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
            filetypes=[("PDF", "*.pdf")]
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
