
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import sys
from datetime import datetime

# Simpan database di folder aplikasi (juga berlaku setelah dibuat menjadi EXE).
BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "space_book.db")


# ==========================================
# DATABASE
# ==========================================

def db():
    return sqlite3.connect(DB)


def setup_db():
    with db() as con:
        cur = con.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS fasilitas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                jenis TEXT NOT NULL,
                harga REAL NOT NULL,
                keterangan TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS booking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                fasilitas_id INTEGER NOT NULL,
                tanggal TEXT NOT NULL,
                jam_mulai TEXT NOT NULL,
                jam_selesai TEXT NOT NULL,
                total REAL NOT NULL,
                status TEXT DEFAULT 'MENUNGGU PEMBAYARAN',
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(fasilitas_id) REFERENCES fasilitas(id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS pembayaran (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id INTEGER NOT NULL,
                metode TEXT NOT NULL,
                jumlah REAL NOT NULL,
                status TEXT DEFAULT 'MENUNGGU VERIFIKASI',
                FOREIGN KEY(booking_id) REFERENCES booking(id)
            )
        """)

        cur.execute(
            "SELECT id FROM users WHERE username='admin'"
        )
        if cur.fetchone() is None:
            cur.execute("""
                INSERT INTO users(username, password, role)
                VALUES ('admin', '1234', 'admin')
            """)

        cur.execute("SELECT COUNT(*) FROM fasilitas")
        if cur.fetchone()[0] == 0:
            data = [
                ("Lapangan Futsal A", "Olahraga", 135000,
                 "Lapangan futsal"),
                ("Lapangan Badminton B", "Olahraga", 50000,
                 "Lapangan badminton"),
                ("Lapngan Basket A", "Olahraga", 175000,
                 "Lapangan Basket"),
                ("Ruang Meeting Beta", "Ruangan", 60000,
                 "Ruang pertemuan")
            ]

            cur.executemany("""
                INSERT INTO fasilitas(nama, jenis, harga, keterangan)
                VALUES (?, ?, ?, ?)
            """, data)


def rupiah(nilai):
    return "Rp{:,.0f}".format(nilai).replace(",", ".")


# ==========================================
# APLIKASI UTAMA
# ==========================================

class SpaceBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SPACE-BOOK | Sistem Booking Fasilitas")
        self.root.geometry("1050x650")
        self.root.minsize(900, 550)

        self.user_id = None
        self.username = None
        self.role = None

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(
            "Treeview",
            rowheight=28,
            font=("Arial", 10)
        )
        self.style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

        self.login_page()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def heading(self, parent, text):
        tk.Label(
            parent,
            text=text,
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#183153"
        ).pack(pady=15)

    def login_page(self):
        self.clear()
        self.root.configure(bg="#eef2f7")

        frame = tk.Frame(
            self.root,
            bg="white",
            padx=45,
            pady=35
        )
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            frame,
            text="SPACE-BOOK",
            font=("Arial", 26, "bold"),
            fg="#183153",
            bg="white"
        ).pack(pady=10)

        tk.Label(
            frame,
            text="Sistem Pemesanan Fasilitas",
            font=("Arial", 11),
            bg="white"
        ).pack(pady=(0, 20))

        tk.Label(frame, text="Username", bg="white").pack(anchor="w")
        self.login_username = tk.Entry(frame, width=35)
        self.login_username.pack(pady=5)

        tk.Label(frame, text="Password", bg="white").pack(anchor="w")
        self.login_password = tk.Entry(
            frame, width=35, show="*"
        )
        self.login_password.pack(pady=5)

        tk.Button(
            frame,
            text="LOGIN",
            width=30,
            bg="#183153",
            fg="white",
            command=self.login
        ).pack(pady=15)

        tk.Button(
            frame,
            text="Daftar Akun Baru",
            width=30,
            command=self.register_page
        ).pack()

        tk.Label(
            frame,
            text="Admin demo: admin / admin123",
            bg="white",
            fg="gray"
        ).pack(pady=15)

    def login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get()

        if not username or not password:
            messagebox.showwarning(
                "Peringatan", "Username dan password harus diisi."
            )
            return

        with db() as con:
            cur = con.cursor()
            cur.execute("""
                SELECT id, username, role
                FROM users
                WHERE username=? AND password=?
            """, (username, password))
            data = cur.fetchone()

        if data:
            self.user_id, self.username, self.role = data
            self.dashboard()
        else:
            messagebox.showerror(
                "Login Gagal", "Username atau password salah."
            )

    def register_page(self):
        self.clear()
        self.root.configure(bg="white")

        frame = tk.Frame(self.root, bg="white", padx=25, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        self.heading(frame, "DAFTAR AKUN BARU")

        tk.Label(frame, text="Username", bg="white").pack()
        username = tk.Entry(frame, width=35)
        username.pack(pady=5)

        tk.Label(frame, text="Password", bg="white").pack()
        password = tk.Entry(frame, width=35, show="*")
        password.pack(pady=5)

        tk.Label(
            frame,
            text="Username minimal 3 karakter\\nPassword minimal 4 karakter",
            bg="white",
            fg="gray"
        ).pack(pady=5)

        def daftar():
            u = username.get().strip()
            p = password.get()

            if not u or not p:
                messagebox.showwarning(
                    "Peringatan", "Username dan password wajib diisi."
                )
                return

            if len(u) < 3:
                messagebox.showwarning(
                    "Peringatan", "Username minimal 3 karakter."
                )
                return

            if len(p) < 4:
                messagebox.showwarning(
                    "Peringatan", "Password minimal 4 karakter."
                )
                return

            try:
                with db() as con:
                    con.execute("""
                        INSERT INTO users(username, password, role)
                        VALUES (?, ?, 'user')
                    """, (u, p))

                messagebox.showinfo(
                    "Berhasil", "Akun berhasil dibuat. Silakan login."
                )
                self.login_page()

            except sqlite3.IntegrityError:
                messagebox.showerror(
                    "Gagal", "Username sudah digunakan."
                )
            except sqlite3.Error as e:
                messagebox.showerror(
                    "Kesalahan Database", f"Terjadi kesalahan: {e}"
                )

        tk.Button(
            frame,
            text="DAFTAR",
            width=25,
            bg="#183153",
            fg="white",
            command=daftar
        ).pack(pady=15)

        tk.Button(
            frame,
            text="Kembali ke Login",
            command=self.login_page
        ).pack()

    # ======================================
    # DASHBOARD
    # ======================================

    def dashboard(self):
        self.clear()
        self.root.configure(bg="#eef2f7")

        header = tk.Frame(self.root, bg="#183153", height=75)
        header.pack(fill="x")

        tk.Label(
            header,
            text="SPACE-BOOK",
            bg="#183153",
            fg="white",
            font=("Arial", 20, "bold")
        ).pack(side="left", padx=25, pady=18)

        tk.Label(
            header,
            text=f"{self.username} ({self.role.upper()})",
            bg="#183153",
            fg="white",
            font=("Arial", 11)
        ).pack(side="right", padx=25)

        body = tk.Frame(self.root, bg="#eef2f7")
        body.pack(fill="both", expand=True, padx=25, pady=20)

        self.heading(body, "DASHBOARD")

        menu = tk.Frame(body, bg="#eef2f7")
        menu.pack(pady=10)

        buttons = [
            ("Daftar Fasilitas", self.facility_page),
            ("Booking Fasilitas", self.booking_page),
            ("Riwayat Booking", self.history_page)
        ]

        if self.role == "admin":
            buttons += [
                ("Kelola Fasilitas", self.manage_facility_page),
                ("Semua Booking", self.all_booking_page),
                ("Verifikasi Pembayaran", self.payment_admin_page),
                ("Laporan", self.report_page)
            ]
        else:
            buttons.append(("Pembayaran", self.payment_page))

        for i, (label, command) in enumerate(buttons):
            tk.Button(
                menu,
                text=label,
                width=27,
                height=2,
                command=command,
                bg="white"
            ).grid(
                row=i // 2,
                column=i % 2,
                padx=10,
                pady=8
            )

        tk.Button(
            body,
            text="LOGOUT",
            width=20,
            bg="#b83232",
            fg="white",
            command=self.logout
        ).pack(pady=20)

    def page(self, title):
        self.clear()
        self.root.configure(bg="white")

        top = tk.Frame(self.root, bg="#183153")
        top.pack(fill="x")

        tk.Label(
            top,
            text=title,
            bg="#183153",
            fg="white",
            font=("Arial", 18, "bold")
        ).pack(side="left", padx=20, pady=15)

        tk.Button(
            top,
            text="Kembali",
            command=self.dashboard
        ).pack(side="right", padx=20, pady=12)

        return tk.Frame(self.root, bg="white", padx=20, pady=15)

    def make_tree(self, parent, columns, headings):
        frame = tk.Frame(parent)
        frame.pack(fill="both", expand=True, pady=10)

        tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        for col, heading in zip(columns, headings):
            tree.heading(col, text=heading)
            tree.column(col, width=120, anchor="center")

        scroll = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=tree.yview
        )
        tree.configure(yscrollcommand=scroll.set)

        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        return tree

    # ======================================
    # DAFTAR FASILITAS
    # ======================================

    def facility_page(self):
        body = self.page("DAFTAR FASILITAS")

        tree = self.make_tree(
            body,
            ("id", "nama", "jenis", "harga", "keterangan"),
            ("ID", "Nama Fasilitas", "Jenis", "Harga/Jam", "Keterangan")
        )

        with db() as con:
            rows = con.execute("""
                SELECT * FROM fasilitas ORDER BY id
            """).fetchall()

        for row in rows:
            tree.insert(
                "", "end",
                values=(
                    row[0], row[1], row[2],
                    rupiah(row[3]), row[4]
                )
            )

        body.pack(fill="both", expand=True)

    # ======================================
    # KELOLA FASILITAS ADMIN
    # ======================================

    def manage_facility_page(self):
        body = self.page("KELOLA FASILITAS")

        form = tk.Frame(body, bg="white")
        form.pack(fill="x", pady=10)

        fields = {}
        labels = ["Nama", "Jenis", "Harga per jam", "Keterangan"]

        for i, label in enumerate(labels):
            tk.Label(
                form, text=label, bg="white"
            ).grid(row=i, column=0, sticky="w", pady=4)

            entry = tk.Entry(form, width=35)
            entry.grid(row=i, column=1, pady=4, padx=10)
            fields[label] = entry

        tree = self.make_tree(
            body,
            ("id", "nama", "jenis", "harga", "keterangan"),
            ("ID", "Nama", "Jenis", "Harga/Jam", "Keterangan")
        )

        def refresh():
            tree.delete(*tree.get_children())
            with db() as con:
                rows = con.execute(
                    "SELECT * FROM fasilitas ORDER BY id"
                ).fetchall()

            for row in rows:
                tree.insert("", "end", values=row)

        def tambah():
            try:
                nama = fields["Nama"].get().strip()
                jenis = fields["Jenis"].get().strip()
                harga = float(fields["Harga per jam"].get())
                ket = fields["Keterangan"].get().strip()

                if not nama or not jenis or harga <= 0:
                    raise ValueError

                with db() as con:
                    con.execute("""
                        INSERT INTO fasilitas(nama, jenis, harga, keterangan)
                        VALUES (?, ?, ?, ?)
                    """, (nama, jenis, harga, ket))

                messagebox.showinfo(
                    "Berhasil", "Fasilitas berhasil ditambahkan."
                )
                for entry in fields.values():
                    entry.delete(0, "end")
                refresh()

            except ValueError:
                messagebox.showerror(
                    "Kesalahan", "Periksa nama, jenis, dan harga."
                )

        def hapus():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning(
                    "Peringatan", "Pilih fasilitas yang ingin dihapus."
                )
                return

            facility_id = tree.item(selected[0])["values"][0]

            if not messagebox.askyesno(
                "Konfirmasi", "Hapus fasilitas ini?"
            ):
                return

            with db() as con:
                used = con.execute("""
                    SELECT COUNT(*) FROM booking
                    WHERE fasilitas_id=?
                """, (facility_id,)).fetchone()[0]

                if used:
                    messagebox.showerror(
                        "Gagal",
                        "Fasilitas sudah memiliki riwayat booking."
                    )
                    return

                con.execute(
                    "DELETE FROM fasilitas WHERE id=?",
                    (facility_id,)
                )

            refresh()

        tk.Button(
            form, text="Tambah Fasilitas",
            command=tambah
        ).grid(row=4, column=1, pady=8, sticky="w")

        tk.Button(
            body, text="Hapus Fasilitas",
            command=hapus
        ).pack(pady=5)

        refresh()
        body.pack(fill="both", expand=True)

    # ======================================
    # BOOKING
    # ======================================

    def booking_page(self):
        body = self.page("BOOKING FASILITAS")

        with db() as con:
            facilities = con.execute("""
                SELECT id, nama, harga FROM fasilitas
                ORDER BY nama
            """).fetchall()

        if not facilities:
            messagebox.showinfo(
                "Informasi", "Belum ada fasilitas tersedia."
            )
            self.dashboard()
            return

        tk.Label(
            body, text="Pilih Fasilitas", bg="white"
        ).pack(anchor="w")

        pilihan = {
            f"{row[1]} - {rupiah(row[2])}/jam": row
            for row in facilities
        }

        combo = ttk.Combobox(
            body,
            values=list(pilihan.keys()),
            state="readonly",
            width=45
        )
        combo.pack(anchor="w", pady=5)
        combo.current(0)

        entries = {}

        for label in [
            "Tanggal (DD-MM-YYYY)",
            "Jam Mulai (HH:MM)",
            "Jam Selesai (HH:MM)"
        ]:
            tk.Label(
                body, text=label, bg="white"
            ).pack(anchor="w", pady=(8, 0))

            entry = tk.Entry(body, width=30)
            entry.pack(anchor="w")
            entries[label] = entry

        def simpan():
            try:
                facility = pilihan[combo.get()]
                facility_id = facility[0]
                harga = float(facility[2])

                tanggal = entries[
                    "Tanggal (DD-MM-YYYY)"
                ].get().strip()

                mulai = entries[
                    "Jam Mulai (HH:MM)"
                ].get().strip()

                selesai = entries[
                    "Jam Selesai (HH:MM)"
                ].get().strip()

                tanggal_obj = datetime.strptime(
                    tanggal, "%d-%m-%Y"
                ).date()

                jam_mulai = datetime.strptime(
                    mulai, "%H:%M"
                )
                jam_selesai = datetime.strptime(
                    selesai, "%H:%M"
                )

                if tanggal_obj < datetime.now().date():
                    messagebox.showerror(
                        "Gagal", "Tanggal tidak boleh di masa lalu."
                    )
                    return

                if jam_selesai <= jam_mulai:
                    messagebox.showerror(
                        "Gagal", "Jam selesai harus setelah jam mulai."
                    )
                    return

                if jam_mulai.hour < 8 or (
                    jam_selesai.hour > 22 or
                    (jam_selesai.hour == 22 and jam_selesai.minute > 0)
                ):
                    messagebox.showerror(
                        "Gagal",
                        "Jam operasional adalah 08:00 sampai 22:00."
                    )
                    return

                durasi = (
                    jam_selesai.hour * 60 + jam_selesai.minute
                    - jam_mulai.hour * 60 - jam_mulai.minute
                ) / 60

                total = durasi * harga

                with db() as con:
                    cur = con.cursor()

                    bentrok = cur.execute("""
                        SELECT COUNT(*) FROM booking
                        WHERE fasilitas_id=?
                        AND tanggal=?
                        AND status != 'DIBATALKAN'
                        AND jam_mulai < ?
                        AND jam_selesai > ?
                    """, (
                        facility_id, tanggal, selesai, mulai
                    )).fetchone()[0]

                    if bentrok:
                        messagebox.showerror(
                            "Jadwal Penuh",
                            "Fasilitas sudah dipesan pada jam tersebut."
                        )
                        return

                    cur.execute("""
                        INSERT INTO booking(
                            user_id, fasilitas_id, tanggal,
                            jam_mulai, jam_selesai, total
                        )
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        self.user_id, facility_id, tanggal,
                        mulai, selesai, total
                    ))

                messagebox.showinfo(
                    "Booking Berhasil",
                    f"Booking berhasil dibuat.\n"
                    f"Durasi: {durasi:g} jam\n"
                    f"Total: {rupiah(total)}\n\n"
                    "Silakan lakukan pembayaran."
                )

                self.dashboard()

            except ValueError:
                messagebox.showerror(
                    "Kesalahan",
                    "Format tanggal atau jam tidak valid.\n"
                    "Contoh tanggal: 25-11-2026\n"
                    "Contoh jam: 09:00"
                )

        tk.Button(
            body,
            text="SIMPAN BOOKING",
            command=simpan,
            bg="#183153",
            fg="white",
            width=25
        ).pack(anchor="w", pady=20)

        body.pack(fill="both", expand=True)

    # ======================================
    # RIWAYAT BOOKING
    # ======================================

    def history_page(self):
        body = self.page("RIWAYAT BOOKING")

        tree = self.make_tree(
            body,
            ("id", "fasilitas", "tanggal", "mulai",
             "selesai", "total", "status"),
            ("ID", "Fasilitas", "Tanggal", "Mulai",
             "Selesai", "Total", "Status")
        )

        with db() as con:
            rows = con.execute("""
                SELECT b.id, f.nama, b.tanggal,
                       b.jam_mulai, b.jam_selesai,
                       b.total, b.status
                FROM booking b
                JOIN fasilitas f ON f.id=b.fasilitas_id
                WHERE b.user_id=?
                ORDER BY b.id DESC
            """, (self.user_id,)).fetchall()

        for row in rows:
            tree.insert(
                "", "end",
                values=(
                    row[0], row[1], row[2], row[3],
                    row[4], rupiah(row[5]), row[6]
                )
            )

        body.pack(fill="both", expand=True)

    # ======================================
    # PEMBAYARAN USER
    # ======================================

    def payment_page(self):
        body = self.page("PEMBAYARAN")

        tree = self.make_tree(
            body,
            ("id", "fasilitas", "tanggal", "total", "status"),
            ("ID Booking", "Fasilitas", "Tanggal", "Total", "Status")
        )

        with db() as con:
            rows = con.execute("""
                SELECT b.id, f.nama, b.tanggal,
                       b.total, b.status
                FROM booking b
                JOIN fasilitas f ON f.id=b.fasilitas_id
                WHERE b.user_id=?
                AND b.status='MENUNGGU PEMBAYARAN'
                ORDER BY b.id DESC
            """, (self.user_id,)).fetchall()

        for row in rows:
            tree.insert(
                "", "end",
                values=(
                    row[0], row[1], row[2],
                    rupiah(row[3]), row[4]
                )
            )

        tk.Label(
            body,
            text="Pilih booking, lalu pilih metode pembayaran.",
            bg="white"
        ).pack(pady=8)

        metode = ttk.Combobox(
            body,
            values=["Transfer", "Bayar di Tempat"],
            state="readonly",
            width=25
        )
        metode.pack()
        metode.current(0)

        def bayar():
            selected = tree.selection()

            if not selected:
                messagebox.showwarning(
                    "Peringatan", "Pilih booking terlebih dahulu."
                )
                return

            booking_id = tree.item(
                selected[0]
            )["values"][0]

            metode_bayar = metode.get()

            with db() as con:
                cur = con.cursor()

                booking = cur.execute("""
                    SELECT total, status FROM booking
                    WHERE id=? AND user_id=?
                """, (booking_id, self.user_id)).fetchone()

                if not booking or booking[1] != "MENUNGGU PEMBAYARAN":
                    messagebox.showerror(
                        "Gagal", "Booking tidak dapat dibayar."
                    )
                    return

                if metode_bayar == "Transfer":
                    status_bayar = "MENUNGGU VERIFIKASI"
                    status_booking = "MENUNGGU VERIFIKASI"
                else:
                    status_bayar = "BELUM LUNAS"
                    status_booking = "BELUM LUNAS"

                cur.execute("""
                    INSERT INTO pembayaran(
                        booking_id, metode, jumlah, status
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    booking_id, metode_bayar,
                    booking[0], status_bayar
                ))

                cur.execute("""
                    UPDATE booking SET status=?
                    WHERE id=?
                """, (status_booking, booking_id))

            messagebox.showinfo(
                "Berhasil",
                "Data pembayaran berhasil disimpan."
            )
            self.payment_page()

        tk.Button(
            body,
            text="PROSES PEMBAYARAN",
            command=bayar
        ).pack(pady=12)

        body.pack(fill="both", expand=True)

    # ======================================
    # SEMUA BOOKING ADMIN
    # ======================================

    def all_booking_page(self):
        body = self.page("SEMUA DATA BOOKING")

        tree = self.make_tree(
            body,
            ("id", "username", "fasilitas", "tanggal",
             "mulai", "selesai", "total", "status"),
            ("ID", "User", "Fasilitas", "Tanggal",
             "Mulai", "Selesai", "Total", "Status")
        )

        with db() as con:
            rows = con.execute("""
                SELECT b.id, u.username, f.nama, b.tanggal,
                       b.jam_mulai, b.jam_selesai,
                       b.total, b.status
                FROM booking b
                JOIN users u ON u.id=b.user_id
                JOIN fasilitas f ON f.id=b.fasilitas_id
                ORDER BY b.id DESC
            """).fetchall()

        for row in rows:
            tree.insert(
                "", "end",
                values=(
                    row[0], row[1], row[2], row[3],
                    row[4], row[5], rupiah(row[6]), row[7]
                )
            )

        body.pack(fill="both", expand=True)

    # ======================================
    # VERIFIKASI PEMBAYARAN ADMIN
    # ======================================

    def payment_admin_page(self):
        body = self.page("VERIFIKASI PEMBAYARAN")

        tree = self.make_tree(
            body,
            ("id", "booking", "username", "metode",
             "jumlah", "status"),
            ("ID Bayar", "ID Booking", "User",
             "Metode", "Jumlah", "Status")
        )

        def refresh():
            tree.delete(*tree.get_children())

            with db() as con:
                rows = con.execute("""
                    SELECT p.id, p.booking_id, u.username,
                           p.metode, p.jumlah, p.status
                    FROM pembayaran p
                    JOIN booking b ON b.id=p.booking_id
                    JOIN users u ON u.id=b.user_id
                    ORDER BY p.id DESC
                """).fetchall()

            for row in rows:
                tree.insert(
                    "", "end",
                    values=(
                        row[0], row[1], row[2],
                        row[3], rupiah(row[4]), row[5]
                    )
                )

        def verifikasi():
            selected = tree.selection()

            if not selected:
                messagebox.showwarning(
                    "Peringatan", "Pilih pembayaran terlebih dahulu."
                )
                return

            values = tree.item(selected[0])["values"]
            payment_id = values[0]
            booking_id = values[1]
            status = values[5]

            if status != "MENUNGGU VERIFIKASI":
                messagebox.showinfo(
                    "Informasi",
                    "Pembayaran ini tidak menunggu verifikasi."
                )
                return

            if not messagebox.askyesno(
                "Konfirmasi", "Verifikasi pembayaran ini?"
            ):
                return

            with db() as con:
                con.execute("""
                    UPDATE pembayaran SET status='LUNAS'
                    WHERE id=?
                """, (payment_id,))

                con.execute("""
                    UPDATE booking SET status='LUNAS'
                    WHERE id=?
                """, (booking_id,))

            messagebox.showinfo(
                "Berhasil", "Pembayaran berhasil diverifikasi."
            )
            refresh()

        tk.Button(
            body,
            text="VERIFIKASI PEMBAYARAN",
            command=verifikasi
        ).pack(pady=10)

        refresh()
        body.pack(fill="both", expand=True)

    # ======================================
    # LAPORAN ADMIN
    # ======================================

    def report_page(self):
        body = self.page("LAPORAN PENYEWAAN")

        with db() as con:
            total_booking = con.execute("""
                SELECT COUNT(*) FROM booking
            """).fetchone()[0]

            booking_lunas = con.execute("""
                SELECT COUNT(*) FROM booking
                WHERE status='LUNAS'
            """).fetchone()[0]

            pendapatan = con.execute("""
                SELECT COALESCE(SUM(total), 0)
                FROM booking WHERE status='LUNAS'
            """).fetchone()[0]

        data = [
            ("Total Booking", total_booking),
            ("Booking Lunas", booking_lunas),
            ("Total Pendapatan", rupiah(pendapatan))
        ]

        for label, value in data:
            tk.Label(
                body,
                text=f"{label}: {value}",
                font=("Arial", 15),
                bg="white"
            ).pack(anchor="w", pady=12)

        body.pack(fill="both", expand=True)

    # ======================================
    # LOGOUT
    # ======================================

    def logout(self):
        if messagebox.askyesno(
            "Logout", "Yakin ingin keluar?"
        ):
            self.user_id = None
            self.username = None
            self.role = None
            self.login_page()


# ==========================================
# MENJALANKAN PROGRAM
# ==========================================

if __name__ == "__main__":
    setup_db()
    root = tk.Tk()
    app = SpaceBookApp(root)
    root.mainloop()
