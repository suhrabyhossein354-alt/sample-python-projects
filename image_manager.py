import os
import sys
import hashlib
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from pathlib import Path
from collections import defaultdict
import threading


# ─── رنگ‌بندی و استایل ───────────────────────────────────────────────
BG        = "#1A1A2E"   # پس‌زمینه اصلی – آبی تیره شبانه
PANEL     = "#16213E"   # پنل‌های کناری
CARD      = "#0F3460"   # کارت‌ها
ACCENT    = "#E94560"   # قرمز تأکیدی
TEXT      = "#EAEAEA"   # متن اصلی
SUBTEXT   = "#8892A4"   # متن فرعی
SUCCESS   = "#4CAF50"
WARNING   = "#FF9800"


def get_image_hash(path):
    """هش MD5 محتوای تصویر برای شناسایی تکراری‌ها"""
    try:
        with Image.open(path) as img:
            img = img.convert("RGB").resize((64, 64))
            return hashlib.md5(img.tobytes()).hexdigest()
    except Exception:
        return None


SUPPORTED = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".tif"}


def find_images(folder):
    imgs = []
    for root, _, files in os.walk(folder):
        for f in files:
            if Path(f).suffix.lower() in SUPPORTED:
                imgs.append(os.path.join(root, f))
    return sorted(imgs)


# ─── پنجره اصلی ──────────────────────────────────────────────────────
class ImageManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("مدیریت عکس‌ها")
        self.geometry("1200x750")
        self.minsize(900, 600)
        self.configure(bg=BG)
        self.option_add("*Font", ("Segoe UI", 10))

        self.folder      = None
        self.images      = []
        self.current_idx = 0
        self.thumb_size  = (160, 120)
        self.thumbs      = {}        # path → PhotoImage
        self.dup_groups  = []        # [[path, path, …], …]
        self.marked_dups = set()     # paths işaretlenmiş

        self._build_ui()
        self._apply_style()

    # ── ساخت رابط ────────────────────────────────────────────────────
    def _build_ui(self):
        # نوار بالایی
        top = tk.Frame(self, bg=PANEL, height=56)
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(top, text="📷  مدیریت عکس‌ها",
                 bg=PANEL, fg=TEXT, font=("Segoe UI", 14, "bold")).pack(side="left", padx=16, pady=12)

        self._btn(top, "📂  انتخاب پوشه", self._pick_folder).pack(side="left", padx=6, pady=10)
        self._btn(top, "🔍  یافتن تکراری‌ها", self._find_duplicates, bg=CARD).pack(side="left", padx=6, pady=10)

        self.status_var = tk.StringVar(value="یک پوشه انتخاب کنید …")
        tk.Label(top, textvariable=self.status_var,
                 bg=PANEL, fg=SUBTEXT, font=("Segoe UI", 9)).pack(side="right", padx=16)

        # نوار تب
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=0, pady=0)

        # تب ۱: مرور عکس‌ها
        self.tab_browse = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(self.tab_browse, text="  مرور عکس‌ها  ")
        self._build_browse_tab()

        # تب ۲: تکراری‌ها
        self.tab_dups = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(self.tab_dups, text="  عکس‌های تکراری  ")
        self._build_dups_tab()

    def _build_browse_tab(self):
        paned = tk.PanedWindow(self.tab_browse, orient="horizontal",
                               bg=BG, sashwidth=6, sashrelief="flat")
        paned.pack(fill="both", expand=True)

        # چپ: گریدِ تصاویر کوچک
        left = tk.Frame(paned, bg=BG)
        paned.add(left, minsize=300)

        ctrl = tk.Frame(left, bg=BG)
        ctrl.pack(fill="x", padx=8, pady=6)
        tk.Label(ctrl, text="تصاویر:", bg=BG, fg=SUBTEXT).pack(side="left")
        self.count_label = tk.Label(ctrl, text="۰ عکس", bg=BG, fg=ACCENT, font=("Segoe UI", 9, "bold"))
        self.count_label.pack(side="left", padx=6)

        canvas_frame = tk.Frame(left, bg=BG)
        canvas_frame.pack(fill="both", expand=True)

        self.grid_canvas = tk.Canvas(canvas_frame, bg=BG, highlightthickness=0)
        vscroll = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.grid_canvas.yview)
        self.grid_canvas.configure(yscrollcommand=vscroll.set)
        vscroll.pack(side="right", fill="y")
        self.grid_canvas.pack(side="left", fill="both", expand=True)

        self.grid_frame = tk.Frame(self.grid_canvas, bg=BG)
        self.grid_win = self.grid_canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")

        self.grid_frame.bind("<Configure>", lambda e: self.grid_canvas.configure(
            scrollregion=self.grid_canvas.bbox("all")))
        self.grid_canvas.bind("<Configure>", self._on_canvas_resize)
        self.grid_canvas.bind("<MouseWheel>", lambda e: self.grid_canvas.yview_scroll(-1*(e.delta//120), "units"))

        # راست: نمایش بزرگ
        right = tk.Frame(paned, bg=PANEL)
        paned.add(right, minsize=380)

        self.preview_label = tk.Label(right, bg=PANEL)
        self.preview_label.pack(expand=True)

        info_frame = tk.Frame(right, bg=PANEL)
        info_frame.pack(fill="x", padx=16, pady=8)

        self.img_name  = tk.Label(info_frame, text="", bg=PANEL, fg=TEXT,  font=("Segoe UI", 10, "bold"), wraplength=340)
        self.img_info  = tk.Label(info_frame, text="", bg=PANEL, fg=SUBTEXT, font=("Segoe UI", 9))
        self.img_name.pack(anchor="w")
        self.img_info.pack(anchor="w")

        nav = tk.Frame(right, bg=PANEL)
        nav.pack(pady=10)
        self._btn(nav, "◀  قبلی", self._prev_img).pack(side="left", padx=8)
        self._btn(nav, "بعدی  ▶", self._next_img).pack(side="left", padx=8)

    def _build_dups_tab(self):
        top = tk.Frame(self.tab_dups, bg=BG)
        top.pack(fill="x", padx=12, pady=8)
        tk.Label(top, text="عکس‌های تکراری یافت‌شده:", bg=BG, fg=TEXT, font=("Segoe UI", 10, "bold")).pack(side="left")
        self.dup_count_label = tk.Label(top, text="", bg=BG, fg=ACCENT, font=("Segoe UI", 9, "bold"))
        self.dup_count_label.pack(side="left", padx=8)

        btn_f = tk.Frame(top, bg=BG)
        btn_f.pack(side="right")
        self._btn(btn_f, "✓  انتخاب تکراری‌ها (نگه‌داشتن اول)", self._auto_select).pack(side="left", padx=4)
        self._btn(btn_f, "🗑  حذف انتخاب‌شده‌ها", self._delete_selected, bg="#7B1F2E").pack(side="left", padx=4)

        # اسکرول‌فریم برای گروه‌های تکراری
        outer = tk.Frame(self.tab_dups, bg=BG)
        outer.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.dup_canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        dup_scroll = ttk.Scrollbar(outer, orient="vertical", command=self.dup_canvas.yview)
        self.dup_canvas.configure(yscrollcommand=dup_scroll.set)
        dup_scroll.pack(side="right", fill="y")
        self.dup_canvas.pack(side="left", fill="both", expand=True)

        self.dup_frame = tk.Frame(self.dup_canvas, bg=BG)
        self.dup_canvas.create_window((0, 0), window=self.dup_frame, anchor="nw")
        self.dup_frame.bind("<Configure>", lambda e: self.dup_canvas.configure(
            scrollregion=self.dup_canvas.bbox("all")))
        self.dup_canvas.bind("<MouseWheel>", lambda e: self.dup_canvas.yview_scroll(-1*(e.delta//120), "units"))

    # ── دکمه استاندارد ────────────────────────────────────────────────
    def _btn(self, parent, text, cmd, bg=ACCENT, fg="white"):
        return tk.Button(parent, text=text, command=cmd,
                         bg=bg, fg=fg, relief="flat", padx=10, pady=5,
                         activebackground="#c73652", activeforeground="white",
                         cursor="hand2", font=("Segoe UI", 9))

    # ── استایل ttk ───────────────────────────────────────────────────
    def _apply_style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TNotebook",       background=BG,    borderwidth=0)
        s.configure("TNotebook.Tab",   background=PANEL, foreground=SUBTEXT,
                    padding=[14, 8], font=("Segoe UI", 10))
        s.map("TNotebook.Tab",
              background=[("selected", CARD)],
              foreground=[("selected", TEXT)])
        s.configure("TScrollbar", background=PANEL, troughcolor=BG, borderwidth=0, arrowsize=14)

    # ── انتخاب پوشه ─────────────────────────────────────────────────
    def _pick_folder(self):
        folder = filedialog.askdirectory(title="انتخاب پوشه عکس‌ها")
        if not folder:
            return
        self.folder = folder
        self.status_var.set("در حال بارگذاری …")
        self.update_idletasks()
        self.images = find_images(folder)
        self.current_idx = 0
        self.thumbs.clear()
        self._refresh_grid()
        n = len(self.images)
        self.count_label.config(text=f"{n} عکس")
        self.status_var.set(f"پوشه: {folder}  |  {n} تصویر")
        if self.images:
            self._show_preview(0)

    # ── گرید تصاویر کوچک ─────────────────────────────────────────────
    def _on_canvas_resize(self, event):
        self.grid_canvas.itemconfig(self.grid_win, width=event.width)
        self._refresh_grid()

    def _refresh_grid(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()

        cols = max(1, (self.grid_canvas.winfo_width() - 10) // (self.thumb_size[0] + 8))

        def load_thumbs():
            for i, path in enumerate(self.images):
                if path not in self.thumbs:
                    try:
                        img = Image.open(path)
                        img.thumbnail(self.thumb_size, Image.LANCZOS)
                        self.thumbs[path] = ImageTk.PhotoImage(img)
                    except Exception:
                        self.thumbs[path] = None
                self.after(0, lambda i=i, path=path: self._add_thumb(i, path, cols))

        threading.Thread(target=load_thumbs, daemon=True).start()

    def _add_thumb(self, i, path, cols):
        row, col = divmod(i, cols)
        frame = tk.Frame(self.grid_frame, bg=BG, padx=3, pady=3)
        frame.grid(row=row, column=col, sticky="nw")

        ph = self.thumbs.get(path)
        if ph:
            lbl = tk.Label(frame, image=ph, bg=CARD, cursor="hand2",
                           relief="flat", bd=2)
        else:
            lbl = tk.Label(frame, text="❌", bg=CARD, width=10, height=5)
        lbl.pack()

        name = os.path.basename(path)
        tk.Label(frame, text=name[:18]+"…" if len(name) > 18 else name,
                 bg=BG, fg=SUBTEXT, font=("Segoe UI", 7), wraplength=self.thumb_size[0]).pack()

        lbl.bind("<Button-1>", lambda e, idx=i: self._show_preview(idx))

    def _show_preview(self, idx):
        self.current_idx = idx
        path = self.images[idx]
        try:
            img = Image.open(path)
            w, h = img.size
            max_w, max_h = 480, 400
            ratio = min(max_w/w, max_h/h, 1)
            img = img.resize((int(w*ratio), int(h*ratio)), Image.LANCZOS)
            ph = ImageTk.PhotoImage(img)
            self.preview_label.configure(image=ph)
            self.preview_label.image = ph

            size_kb = os.path.getsize(path) // 1024
            self.img_name.config(text=os.path.basename(path))
            self.img_info.config(text=f"{w}×{h}  |  {size_kb} KB  |  {Path(path).suffix.upper()[1:]}")
        except Exception as ex:
            self.img_name.config(text=f"خطا: {ex}")

    def _prev_img(self):
        if self.images:
            self._show_preview((self.current_idx - 1) % len(self.images))

    def _next_img(self):
        if self.images:
            self._show_preview((self.current_idx + 1) % len(self.images))

    # ── یافتن تکراری‌ها ──────────────────────────────────────────────
    def _find_duplicates(self):
        if not self.images:
            messagebox.showwarning("توجه", "ابتدا یک پوشه انتخاب کنید.")
            return

        self.status_var.set("در حال بررسی تکراری‌ها …")
        self.update_idletasks()

        def worker():
            hashes = defaultdict(list)
            for path in self.images:
                h = get_image_hash(path)
                if h:
                    hashes[h].append(path)
            groups = [v for v in hashes.values() if len(v) > 1]
            self.after(0, lambda: self._show_duplicates(groups))

        threading.Thread(target=worker, daemon=True).start()

    def _show_duplicates(self, groups):
        self.dup_groups = groups
        self.marked_dups.clear()

        for w in self.dup_frame.winfo_children():
            w.destroy()

        if not groups:
            tk.Label(self.dup_frame, text="🎉  هیچ تکراری یافت نشد!",
                     bg=BG, fg=SUCCESS, font=("Segoe UI", 14, "bold")).pack(pady=40)
            self.dup_count_label.config(text="بدون تکراری")
            self.status_var.set("بررسی انجام شد – تکراری یافت نشد.")
            self.notebook.select(self.tab_dups)
            return

        total = sum(len(g)-1 for g in groups)
        self.dup_count_label.config(text=f"{len(groups)} گروه  |  {total} فایل اضافه")
        self.status_var.set(f"{len(groups)} گروه تکراری یافت شد")

        self.dup_checks = {}   # path → BooleanVar

        for gi, group in enumerate(groups):
            grp_frame = tk.LabelFrame(self.dup_frame,
                                      text=f"  گروه {gi+1}  ({len(group)} عکس مشابه)  ",
                                      bg=BG, fg=ACCENT,
                                      font=("Segoe UI", 9, "bold"),
                                      labelanchor="nw", bd=1,
                                      relief="groove",
                                      padx=8, pady=6)
            grp_frame.pack(fill="x", padx=10, pady=6)

            for pi, path in enumerate(group):
                row = tk.Frame(grp_frame, bg=CARD if pi % 2 == 0 else BG)
                row.pack(fill="x", pady=1)

                var = tk.BooleanVar()
                self.dup_checks[path] = var
                cb = tk.Checkbutton(row, variable=var, bg=row["bg"],
                                    activebackground=row["bg"],
                                    selectcolor=CARD, fg=ACCENT,
                                    command=lambda p=path, v=var: self._toggle_dup(p, v))
                cb.pack(side="left", padx=6)

                # تصویر کوچک
                try:
                    img = Image.open(path)
                    img.thumbnail((80, 60), Image.LANCZOS)
                    ph = ImageTk.PhotoImage(img)
                    lbl_img = tk.Label(row, image=ph, bg=row["bg"])
                    lbl_img.image = ph
                    lbl_img.pack(side="left", padx=4, pady=2)
                except Exception:
                    pass

                info = tk.Frame(row, bg=row["bg"])
                info.pack(side="left", fill="x", expand=True, padx=6)
                size_kb = os.path.getsize(path) // 1024
                tk.Label(info, text=os.path.basename(path),
                         bg=row["bg"], fg=TEXT, font=("Segoe UI", 9, "bold")).pack(anchor="w")
                tk.Label(info, text=f"{path}  |  {size_kb} KB",
                         bg=row["bg"], fg=SUBTEXT, font=("Segoe UI", 8)).pack(anchor="w")

                tag = tk.Label(row, text="اصلی" if pi == 0 else "تکراری",
                               bg=SUCCESS if pi == 0 else WARNING,
                               fg="white", font=("Segoe UI", 8, "bold"),
                               padx=6, pady=2)
                tag.pack(side="right", padx=8)

        self.notebook.select(self.tab_dups)

    def _toggle_dup(self, path, var):
        if var.get():
            self.marked_dups.add(path)
        else:
            self.marked_dups.discard(path)

    def _auto_select(self):
        """در هر گروه اولین تصویر را نگه می‌داریم و بقیه را تیک می‌زنیم"""
        for group in self.dup_groups:
            for pi, path in enumerate(group):
                if path in self.dup_checks:
                    v = pi > 0
                    self.dup_checks[path].set(v)
                    if v:
                        self.marked_dups.add(path)
                    else:
                        self.marked_dups.discard(path)

    def _delete_selected(self):
        if not self.marked_dups:
            messagebox.showinfo("توجه", "هیچ فایلی انتخاب نشده.")
            return
        n = len(self.marked_dups)
        if not messagebox.askyesno("تأیید حذف",
                                    f"آیا مطمئن هستید که می‌خواهید {n} فایل را حذف کنید؟\nاین عمل قابل بازگشت نیست."):
            return

        errors = []
        for path in list(self.marked_dups):
            try:
                os.remove(path)
                if path in self.images:
                    self.images.remove(path)
            except Exception as e:
                errors.append(f"{path}: {e}")

        self.marked_dups.clear()
        self.status_var.set(f"{n} فایل حذف شد.")
        if errors:
            messagebox.showerror("خطا در حذف", "\n".join(errors))
        else:
            messagebox.showinfo("موفق", f"{n} فایل تکراری با موفقیت حذف شد!")

        # به‌روزرسانی گرید
        self.count_label.config(text=f"{len(self.images)} عکس")
        self._refresh_grid()
        self._find_duplicates()


# ── اجرا ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        from PIL import Image, ImageTk
    except ImportError:
        print("لطفاً Pillow را نصب کنید:  pip install Pillow")
        sys.exit(1)

    app = ImageManager()
    app.mainloop()
