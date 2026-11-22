
# ==========================================
# MATERI 12 - 
# ==========================================


# ==========================================
# MODUL ARITMATIKA
# ==========================================

def penjumlahan(a, b):
    return a + b


def perpangkatan(a, b):
    return a ** b


def perkalian(a, b):
    return a * b


# ==========================================
# MODUL KONVERSI
# ==========================================

def cm_to_m(nilai):
    return nilai / 100


def m_to_cm(nilai):
    return nilai * 100


# ==========================================
# MODUL UBAH BILANGAN
# ==========================================

def desimal_ke_biner(nilai):
    return bin(nilai)[2:]


def desimal_ke_oktal(nilai):
    return oct(nilai)[2:]


def desimal_ke_heksadesimal(nilai):
    return hex(nilai)[2:].upper()


# ==========================================
# MENU ARITMATIKA
# ==========================================

def menu_aritmatika():
    while True:
        print("\n===== MENU ARITMATIKA =====")
        print("1. Penjumlahan")
        print("2. Perpangkatan")
        print("3. Perkalian")
        print("4. Kembali ke menu utama")

        pilihan = input("Pilih menu: ")

        if pilihan == "4":
            break

        if pilihan not in ("1", "2", "3"):
            print("Pilihan tidak tersedia.")
            continue

        try:
            a = float(input("Masukkan bilangan pertama: "))
            b = float(input("Masukkan bilangan kedua: "))

            if pilihan == "1":
                hasil = penjumlahan(a, b)

            elif pilihan == "2":
                hasil = perpangkatan(a, b)

            else:
                hasil = perkalian(a, b)

            print("Hasil:", hasil)

        except ValueError:
            print("Input harus berupa angka.")


# ==========================================
# MENU KONVERSI
# ==========================================

def menu_konversi():
    while True:
        print("\n===== MENU KONVERSI =====")
        print("1. CM to M")
        print("2. M to CM")
        print("3. Kembali ke menu utama")

        pilihan = input("Pilih menu: ")

        if pilihan == "3":
            break

        if pilihan not in ("1", "2"):
            print("Pilihan tidak tersedia.")
            continue

        try:
            nilai = float(input("Masukkan nilai: "))

            if pilihan == "1":
                hasil = cm_to_m(nilai)
                print(nilai, "CM =", hasil, "M")

            else:
                hasil = m_to_cm(nilai)
                print(nilai, "M =", hasil, "CM")

        except ValueError:
            print("Input harus berupa angka.")


# ==========================================
# MENU UBAH BILANGAN
# ==========================================

def menu_ubah_bilangan():
    while True:
        print("\n===== MENU UBAH BILANGAN =====")
        print("1. Desimal to Biner")
        print("2. Desimal to Oktal")
        print("3. Desimal to Heksadesimal")
        print("4. Kembali ke menu utama")

        pilihan = input("Pilih menu: ")

        if pilihan == "4":
            break

        if pilihan not in ("1", "2", "3"):
            print("Pilihan tidak tersedia.")
            continue

        try:
            nilai = int(input("Masukkan bilangan desimal bulat: "))

            if pilihan == "1":
                hasil = desimal_ke_biner(nilai)
                nama = "Biner"

            elif pilihan == "2":
                hasil = desimal_ke_oktal(nilai)
                nama = "Oktal"

            else:
                hasil = desimal_ke_heksadesimal(nilai)
                nama = "Heksadesimal"

            print("Hasil", nama, ":", hasil)

        except ValueError:
            print("Masukkan bilangan bulat yang valid.")


# ==========================================
# MENU UTAMA
# ==========================================

def main():
    while True:
        print("\n===================================")
        print("       PROGRAM MODULAR PYTHON")
        print("===================================")
        print("1. Aritmatika")
        print("2. Konversi")
        print("3. Ubah Bilangan")
        print("4. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            menu_aritmatika()

        elif pilihan == "2":
            menu_konversi()

        elif pilihan == "3":
            menu_ubah_bilangan()

        elif pilihan == "4":
            print("\nTerima kasih telah menggunakan program!")
            break

        else:
            print("Pilihan tidak tersedia. Silakan pilih 1 sampai 4.")


# ==========================================
# MENJALANKAN PROGRAM
# ==========================================

if __name__ == "__main__":
    main()
