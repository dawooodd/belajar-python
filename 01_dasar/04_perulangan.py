"""
================================================================================
MODUL 01: DASAR PEMROGRAMAN PYTHON
FILE 04: Perulangan (Loops), Enumerate, Zip & For-Else Architecture
================================================================================
Tujuan Pembelajaran:
1. Menguasai for loop dan while loop serta optimasinya.
2. Penggunaan iterator bawaan: range(), enumerate(), dan zip().
3. Kontrol alur: break, continue, pass.
4. Memahami fitur unik Python: for...else dan while...else.
5. Menghindari kesalahan umum: Infinite loop dan modifikasi list saat di-loop.
================================================================================
"""

from itertools import zip_longest

print("=" * 70)
print("--- [1] For Loop & Fungsi range() ---")

# range(start, stop_exclusive, step)
print("Deret angka ganjil 1 s/d 10:")
for angka in range(1, 10, 2):
    print(angka, end=" ")
print()

# Iterasi mundur
print("Hitung mundur roket:")
for detik in range(5, 0, -1):
    print(f"{detik}...", end=" ")
print("Meluncur! 🚀")


# ------------------------------------------------------------------------------
# 2. enumerate(): Mengakses Index dan Elemen secara Pythonic
# ------------------------------------------------------------------------------
print("\n--- [2] enumerate() Pattern ---")
bahasa_pemrograman = ["Python", "Rust", "Go", "TypeScript", "SQL"]

# ❌ BAD PRACTICE (C-style):
# for i in range(len(bahasa_pemrograman)):
#     print(f"{i}: {bahasa_pemrograman[i]}")

# ✅ BEST PRACTICE:
for peringkat, bahasa in enumerate(bahasa_pemrograman, start=1):
    print(f"Top #{peringkat}: {bahasa}")


# ------------------------------------------------------------------------------
# 3. zip() & itertools.zip_longest(): Iterasi Multi-Koleksi
# ------------------------------------------------------------------------------
print("\n--- [3] zip() & zip_longest() ---")
nama_siswa = ["Ahmad", "Budi", "Citra"]
nilai_ujian = [88, 95, 91]
status_hadir = [True, True]  # Elemen lebih sedikit

# zip() berhenti pada koleksi terpendek
print("Menggunakan zip() standar (berhenti di terpendek):")
for nama, nilai in zip(nama_siswa, nilai_ujian):
    print(f"- {nama} mendapat nilai: {nilai}")

# zip_longest() mengisi kekosongan dengan fillvalue
print("\nPerbandingan dengan zip_longest:")
for nama, hadir in zip_longest(nama_siswa, status_hadir, fillvalue=False):
    print(f"- {nama} hadir: {hadir}")


# ------------------------------------------------------------------------------
# 4. Fitur Unik: for...else dan while...else
# ------------------------------------------------------------------------------
print("\n--- [4] For-Else Pattern (Pencarian Tanpa Flag) ---")
# Blok 'else' pada for/while akan dieksekusi JIKA DAN HANYA JIKA perulangan
# selesai secara normal (TIDAK terinterupsi oleh 'break').

def cari_bilangan_prima(angka_cek: int) -> bool:
    if angka_cek < 2:
        return False
    
    for pembagi in range(2, int(angka_cek**0.5) + 1):
        if angka_cek % pembagi == 0:
            print(f"❌ {angka_cek} BUKAN bilangan prima (habis dibagi {pembagi})")
            break
    else:
        # Dijalankan HANYA jika tidak ada 'break' sama sekali
        print(f"✅ {angka_cek} ADALAH bilangan prima!")
        return True
    return False

cari_bilangan_prima(29)
cari_bilangan_prima(35)


# ------------------------------------------------------------------------------
# 5. Modifikasi List Saat Looping (Common Pitfall)
# ------------------------------------------------------------------------------
print("\n--- [5] Menghindari Bug Modifikasi List Saat Iterasi ---")
daftar_angka = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# ❌ JANGAN PERNAH MENGHAPUS ELEMEN LANGSUNG DARI LIST YANG SEDANG DIITERASI:
# for x in daftar_angka:
#     if x % 2 == 0:
#         daftar_angka.remove(x) # Ini akan melewatkan elemen karena index bergeser!

# ✅ SOLUSI 1: Iterasi pada shallow copy (daftar_angka[:])
# ✅ SOLUSI 2: Buat list baru via list comprehension (paling direkomendasikan):
angka_ganjil = [x for x in daftar_angka if x % 2 != 0]
print(f"Hasil filtering aman: {angka_ganjil}")


# ------------------------------------------------------------------------------
# 6. While Loop dengan Kontrol Fleksibel
# ------------------------------------------------------------------------------
print("\n--- [6] While Loop & Sentinel Pattern ---")
saldo_token = 50
biaya_request = 15
request_ke = 1

while saldo_token >= biaya_request:
    saldo_token -= biaya_request
    print(f"Request #{request_ke} berhasil! Sisa token: {saldo_token}")
    request_ke += 1
else:
    print(f"Selesai: Saldo token ({saldo_token}) tidak cukup untuk request berikutnya.")


print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 04:")
print("1. Hindari `for i in range(len(x))` — gunakan `enumerate()` jika butuh index.")
print("2. Gunakan `zip()` untuk memasangkan dua atau lebih iterables secara paralel.")
print("3. Manfaatkan `for ... else` untuk logika pencarian (search loops) agar kode bebas dari variabel flag.")
print("4. Jangan pernah memutasi koleksi (remove/pop) langsung dalam perulangan yang sedang berjalan.")
print("=" * 70)
