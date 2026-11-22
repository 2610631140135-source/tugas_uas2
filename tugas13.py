
# ==========================================
# MATERI 13 - EXCEPTION HANDLING
# PROGRAM PENGECEKAN DATA MAHASISWA
# ==========================================


# ==========================================
# 1. INPUT DAN PENGECEKAN NILAI
# ==========================================

def cek_nilai():
    print("\n=== PENGECEKAN NILAI MAHASISWA ===")

    try:
        nilai = float(input("Masukkan nilai mahasiswa: "))

        if nilai < 0 or nilai > 100:
            raise ValueError("Nilai harus berada antara 0 sampai 100.")

    except ValueError as error:
        print("Terjadi kesalahan:", error)

    else:
        print("Nilai berhasil dimasukkan:", nilai)

        if nilai >= 75:
            print("Keterangan: Lulus")
        else:
            print("Keterangan: Tidak lulus")

        print("Blok else dijalankan karena input benar.")

    finally:
        print("Pengecekan nilai selesai.")


# ==========================================
# 2. MENGAKSES DATA MAHASISWA
# ==========================================

def akses_data():
    print("\n=== DATA MAHASISWA ===")

    mahasiswa = ["Andi", "Budi", "Citra", "Dina", "Eka"]

    try:
        nomor = int(input("Masukkan nomor data (0 sampai 4): "))

        print("Nama mahasiswa:", mahasiswa[nomor])

    except ValueError:
        print("ValueError: nomor harus berupa bilangan bulat.")

    except IndexError:
        print("IndexError: nomor data tidak ditemukan.")

    else:
        print("Data berhasil ditemukan.")

    finally:
        print("Proses akses data selesai.")


# ==========================================
# 3. MENGHITUNG RATA-RATA NILAI
# ==========================================

def rata_rata():
    print("\n=== MENGHITUNG RATA-RATA ===")

    try:
        nilai1 = float(input("Masukkan nilai pertama: "))
        nilai2 = float(input("Masukkan nilai kedua: "))
        nilai3 = float(input("Masukkan nilai ketiga: "))

        if not all(0 <= n <= 100 for n in (nilai1, nilai2, nilai3)):
            raise ValueError("Semua nilai harus antara 0 sampai 100.")

        total = nilai1 + nilai2 + nilai3
        hasil = total / 3

    except ValueError as error:
        print("Terjadi kesalahan:", error)

    else:
        print("Total nilai:", total)
        print("Nilai rata-rata:", round(hasil, 2))

    finally:
        print("Perhitungan rata-rata selesai.")


# ==========================================
# 4. MENU UTAMA
# ==========================================

def main():
    while True:
        print("\n================================")
        print("  PROGRAM DATA MAHASISWA")
        print("================================")
        print("1. Pengecekan Nilai")
        print("2. Akses Data Mahasiswa")
        print("3. Hitung Rata-rata")
        print("4. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            cek_nilai()

        elif pilihan == "2":
            akses_data()

        elif pilihan == "3":
            rata_rata()

        elif pilihan == "4":
            print("Program selesai. Terima kasih!")
            break

        else:
            print("Pilihan tidak valid.")


# ==========================================
# MENJALANKAN PROGRAM
# ==========================================

if __name__ == "__main__":
    main()
