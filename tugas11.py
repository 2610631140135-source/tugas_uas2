
# ==========================================
# MATERI 11 - FUNCTION DAN MANIPULASI STRING
# PROGRAM PENGOLAHAN TEKS
# ==========================================

def hitung_kata(kalimat):
    """Menghitung jumlah kata dalam kalimat."""
    kata = kalimat.split()
    return len(kata)


def balik_kalimat(kalimat):
    """Membalik seluruh karakter dalam kalimat."""
    return kalimat[::-1]


def ubah_kapital(kalimat):
    """Mengubah semua huruf menjadi kapital."""
    return kalimat.upper()


def ganti_huruf(kalimat, huruf_lama, huruf_baru):
    """Mengganti huruf tertentu dalam kalimat."""
    hasil = ""
    for karakter in kalimat:
        if karakter == huruf_lama:
            hasil += huruf_baru
        else:
            hasil += karakter
    return hasil


# ==========================================
# PROGRAM UTAMA
# ==========================================

if __name__ == "__main__":

    print("=== PROGRAM PENGOLAHAN TEKS ===")

    teks = input("Masukkan sebuah kalimat: ")

    print("\n1. Jumlah kata:")
    print(hitung_kata(teks))

    print("\n2. Kalimat terbalik:")
    print(balik_kalimat(teks))

    print("\n3. Huruf kapital:")
    print(ubah_kapital(teks))

    print("\n4. Mengganti huruf:")
    lama = input("Huruf yang ingin diganti: ")
    baru = input("Huruf pengganti: ")

    print("Hasil:", ganti_huruf(teks, lama, baru))
